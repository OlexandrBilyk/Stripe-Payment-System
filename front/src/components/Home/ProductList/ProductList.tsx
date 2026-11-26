'use client'

import Product from "../Product/Product"
import { useGetProductsQuery } from "@/redux/productApi/productApi"

export default function ProductList() {
    const { data } = useGetProductsQuery()


    return (
        <ul>
            {data?.map((el) => (
                <li key={el.id}>
                    <Product id={el.id}></Product>
                </li>
            ))}
        </ul>
    )
}