import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQueryWithReauth } from "../baseQuery";
import type { Product } from "@/types/product";

export const productApi = createApi({
    reducerPath: "product",
    baseQuery: baseQueryWithReauth,
    endpoints: (builder) => ({
        getProducts: builder.query<Product[], void>({
            query: () => "/product/product"
        }),
        getProductById: builder.query<Product, number>({
            query: (id) => `/product/product/${id}`
        }),
    })
})

export const { useGetProductsQuery, useGetProductByIdQuery } = productApi