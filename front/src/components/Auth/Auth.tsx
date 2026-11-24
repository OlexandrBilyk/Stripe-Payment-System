'use client'

import AuthForm from "./AuthForm/AuthForm"
import { useState } from "react"


export default function Auth() {
    const [type, setType] = useState<"register" | "login">("login")

    return (
        <>
            <AuthForm type={type}></AuthForm>
            <button type="button" onClick={() => type !== "register" ? setType('register') : ''}>register</button>
            <button type="button" onClick={() => type !== "login" ? setType('login') : ''}>login</button>
        </>
    )
}