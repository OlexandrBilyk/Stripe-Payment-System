
import {
    fetchBaseQuery,
    type BaseQueryFn,
    type FetchArgs,
    type FetchBaseQueryError,
} from "@reduxjs/toolkit/query/react";

export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

const baseQuery = fetchBaseQuery({
    baseUrl: BACKEND_URL,
    credentials: "include",
});

let refreshPromise: Promise<boolean> | null = null;
let logoutPromise: Promise<void> | null = null;

export const baseQueryWithReauth: BaseQueryFn<
    string | FetchArgs,
    unknown,
    FetchBaseQueryError
> = async (args, api, extraOptions) => {

    let result = await baseQuery(args, api, extraOptions);

    if (result.error?.status !== 401) {
        return result;
    }

    const url = typeof args === "string" ? args : args.url;

    if (url.startsWith("/auth/")) {
        return result;
    }

    if (!refreshPromise) {
        refreshPromise = (async () => {
            try {
                const refreshResult = await baseQuery(
                    "/auth/refresh/",
                    api,
                    extraOptions
                );

                return !refreshResult.error;
            } catch {
                return false;
            }
        })();
    }

    const currentRefresh = refreshPromise;

    let refreshed = false;

    try {
        refreshed = await currentRefresh;
    } finally {
        if (refreshPromise === currentRefresh) {
            refreshPromise = null;
        }
    }
    if (refreshed) {
        return await baseQuery(args, api, extraOptions);
    }

    if (!logoutPromise) {
        logoutPromise = (async () => {
            try {
                await baseQuery(
                    "/auth/logout/",
                    api,
                    extraOptions
                );
            } finally {
                if (typeof window !== "undefined") {
                    window.location.assign("/auth");
                }
            }
        })();
    }

    await logoutPromise;

    return result;
};
