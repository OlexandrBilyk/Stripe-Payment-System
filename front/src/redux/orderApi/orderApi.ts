import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQueryWithReauth } from "../baseQuery";

type ResType = {
    id: string,
    status: string,
    client_secret: string
}

export const orderApi = createApi({
    reducerPath: 'order',
    baseQuery: baseQueryWithReauth,
    endpoints: (builder) => ({
        postOrder: builder.mutation<ResType, number>({
            query: (productId) => ({
                url: '/checkout/order',
                body: productId,
                method: 'POST'
            })
        })
    })
})


export const { usePostOrderMutation } = orderApi