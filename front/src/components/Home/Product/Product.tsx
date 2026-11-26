'use client'

import type { Product } from "@/types/product"
import { useGetProductByIdQuery } from "@/redux/productApi/productApi"
import { useAddProductToCartMutation } from "@/redux/profileApi/profileApi"
import { useRouter } from "next/navigation"

type ProductProps = Omit<Product, "name" | "price">

export default function Product({ id }: ProductProps) {
    const { data } = useGetProductByIdQuery(id)
    const [addProduct] = useAddProductToCartMutation()
    const router = useRouter()

    const handleProduct = async function () {
        try {
            const product_data = { product_id: id, quantity: 1 }

            const res = await addProduct(product_data).unwrap()

            router.push('/cart')

        } catch (err) {
            console.log(err);
        }
    }

    return (
        <div>
            <h3>{data?.name}</h3>
            <p>{data?.price}</p>
            <button type="button" onClick={handleProduct}>Add to cart</button>
        </div>
    )
}