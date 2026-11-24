import { baseQueryWithReauth } from "../baseQuery";
import { createApi } from "@reduxjs/toolkit/query/react";


export const profileApi = createApi({
    reducerPath: "profile",
    baseQuery: baseQueryWithReauth,
    endpoints: (builder) => ({
        getProfile: builder.query<void, void>({
            query: () => '/profile/profile'
        })
    })
})

export const { useGetProfileQuery } = profileApi;