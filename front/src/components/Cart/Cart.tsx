'use client'

import { useGetCartQuery } from "@/redux/profileApi/profileApi"
import CartItem from "../CartItem/CartItem"
import { useRouter } from "next/navigation"

export default function Cart() {
    const { data } = useGetCartQuery()
    const router = useRouter()


    const handleBack = function () {
        router.back()
    }


    return (
        <>
            <button type="button" onClick={handleBack}>back</button>

            {data?.cart_items.map((el) => (
                <li key={el.id}>
                    <CartItem product={el.product} quantity={el.quantity}></CartItem>
                </li>
            ))}
        </>
    )
}