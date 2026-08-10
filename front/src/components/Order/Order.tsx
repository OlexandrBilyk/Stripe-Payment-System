'use client'

import { usePostOrderMutation } from "@/redux/orderApi/orderApi"
import { useState } from "react"
import CheckoutForm from "../CheckoutForm/CheckoutFotm"
import { Elements } from "@stripe/react-stripe-js"
import { stripePromise } from "@/lib/stripe"

type ResType = {
    id: string,
    status: string,
    client_secret: string
}

export default function Order() {
    const [makeOrder] = usePostOrderMutation()
    const [value, setValue] = useState('')
    const [res, setRes] = useState<ResType>()

    const handleClick = async function () {
        try {
            const res = await makeOrder(Number(value)).unwrap()

            setRes(res)
        } catch (err) {
            console.log(err)
        }
    }


    return (
        <>
            <input type="text" value={value} onChange={(e) => setValue(e.target.value)} />

            <button type="button" onClick={handleClick}>Створити замовлення</button>



            {res &&
                <Elements stripe={stripePromise} options={{ clientSecret: res?.client_secret }}>
                    <CheckoutForm></CheckoutForm>
                </Elements >}
        </>
    )
}