import { baseQueryWithReauth } from "../baseQuery";
import { createApi } from "@reduxjs/toolkit/query/react";
import type { CustomerProfile } from "@/types/customer";
import type { Cart, CartItem } from "@/types/cart";

type CartItemAdd = {
    product_id: number,
    quantity: number,
}


export const profileApi = createApi({
    reducerPath: "profile",
    baseQuery: baseQueryWithReauth,
    tagTypes: ['Cart'],
    endpoints: (builder) => ({
        getProfile: builder.query<CustomerProfile, void>({
            query: () => '/profile/profile'
        }),
        getCart: builder.query<Cart, void>({
            query: () => '/profile/cart',
            providesTags: ['Cart']
        }),
        addProductToCart: builder.mutation<Cart, CartItemAdd>({
            query: (body) => ({
                url: "/profile/cart",
                method: "POST",
                body: body
            }),
            invalidatesTags: ['Cart'],
        }),
        changeProductQuantity: builder.mutation<Cart, CartItemAdd>({
            query: (body) => ({
                url: "/profile/cart",
                method: "PATCH",
                body: body
            }),
            invalidatesTags: ['Cart'],
        }),

    })
})

export const { useGetProfileQuery, useGetCartQuery, useAddProductToCartMutation, useChangeProductQuantityMutation } = profileApi;