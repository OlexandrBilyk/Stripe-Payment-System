import { createApi } from "@reduxjs/toolkit/query/react";
import type { BaseResponse } from "@/types/base";
import type { CustomerRegister, CustomerLogin } from "@/types/customer";
import { baseQueryWithReauth } from "../baseQuery";

export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL

export const authApi = createApi({
    reducerPath: 'auth',
    baseQuery: baseQueryWithReauth,
    endpoints: (builder) => ({
        register: builder.mutation<BaseResponse, CustomerRegister>({
            query: (customer) => ({
                url: '/auth/register/',
                method: 'POST',
                body: customer
            })
        }),

        login: builder.mutation<BaseResponse, CustomerLogin>({
            query: (customer) => ({
                url: '/auth/login/',
                method: 'POST',
                body: customer
            })
        }),

        logout: builder.query<BaseResponse, void>({
            query: () => '/auth/logout/'
        }),

        refresh: builder.query<BaseResponse, void>({
            query: () => '/auth/refresh/'
        })
    })
})

export const { useRegisterMutation, useLoginMutation, useLazyLogoutQuery } = authApi