'use client'

import React from "react"
import { useAddProductToCartMutation, useChangeProductQuantityMutation } from "@/redux/profileApi/profileApi"
import type { Product } from "@/types/product"
import debounce from "lodash/debounce"
import { useRef, useEffect } from "react"

type CartItemProps = {
    product: Product,
    quantity: number
}

export default function CartItem({ product, quantity }: CartItemProps) {
    const [changeProductQuantity] = useChangeProductQuantityMutation()
    const inputRef = useRef<HTMLInputElement>(null)

    useEffect(() => {
        if (inputRef.current) {
            inputRef.current.value = String(quantity)
        }
    }, [quantity])

    const handleQuantityChange = debounce(async function (e: React.ChangeEvent<HTMLInputElement>) {
        try {
            if (Number(e.target.value) <= 0) return


            const product_data = {
                product_id: product.id,
                quantity: Number(e.target.value),
            }

            const res = await changeProductQuantity(product_data)

        } catch (err) {
            console.log(err)
        }
    }, 1000)

    const handleQuantity = async function (type: "increase" | "decrease") {
        try {
            if (type == "decrease" && quantity == 1) return

            const product_data = {
                product_id: product.id,
                quantity: type == "increase" ? quantity + 1 : quantity - 1,
            }



            const res = await changeProductQuantity(product_data)

        } catch (err) {
            console.log(err)
        }
    }


    return (
        <div>
            <h2>{product.name}</h2>
            <p>{product.price}</p>
            <input type="number"
                ref={inputRef}
                defaultValue={quantity}
                onChange={handleQuantityChange}
            />
            <button
                type="button"
                onClick={() => handleQuantity("increase")}
            >
                +
            </button>
            <button
                type="button"
                onClick={() => handleQuantity("decrease")}
            >
                -
            </button>
        </div>
    )
}