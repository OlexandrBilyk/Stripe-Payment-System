import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

type ResType = {
    id: string,
    status: string,
    client_secret: string
}

export const orderApi = createApi({
    reducerPath: 'order',
    baseQuery: fetchBaseQuery({ baseUrl: 'http://localhost:8000/checkout', credentials: 'include' }),
    endpoints: (builder) => ({
        postOrder: builder.mutation<ResType, number>({
            query: (productId) => ({
                url: '/order',
                body: productId,
                method: 'POST'
            })
        })
    })
})


export const { usePostOrderMutation } = orderApi