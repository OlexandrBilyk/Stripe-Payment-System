'use client'
import { PaymentElement, useElements, useStripe } from "@stripe/react-stripe-js"
import React from "react"

export default function CheckoutForm() {
    const stripe = useStripe()
    const elements = useElements()

    const handleSubmit = async function (e: React.SubmitEvent) {
        e.preventDefault()

        if (!elements || !stripe) return

        await stripe?.confirmPayment({
            elements,
            confirmParams: {
                return_url: 'http://localhost:3000/success'
            }
        })
    }

    return (
        <form onSubmit={handleSubmit}>
            <PaymentElement></PaymentElement>

            <button type="submit">
                Pay for Nothing 😏😏😏
            </button>
        </form>
    )
}