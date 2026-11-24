'use client'

import AuthGoogle from "../AuthGoogle/AuthGoogle"
import { useForm } from "react-hook-form"
import { useLoginMutation, useRegisterMutation } from "@/redux/authApi/authApi"
import type { CustomerLogin, CustomerRegister } from "@/types/customer"
import { useRouter } from "next/navigation"
import { BACKEND_URL } from "@/redux/authApi/authApi"

type AuthFormProps = {
    type: 'login' | 'register'
}

export default function AuthForm({ type }: AuthFormProps) {
    const { register, handleSubmit } = useForm<CustomerRegister | CustomerLogin>()

    const [registerCustomer] = useRegisterMutation()
    const [loginCustomer] = useLoginMutation()

    const router = useRouter()


    const onSubmit = async function (values: CustomerRegister | CustomerLogin) {
        try {
            if (type === 'register') {
                const res = await registerCustomer(values as CustomerRegister).unwrap()

                router.replace('/')
            } else {
                const res = await loginCustomer(values as CustomerLogin).unwrap()

                router.replace('/')
            }
        } catch (err) {
            console.log(err)
        }
    }

    return (
        <>
            <div>
                <p>
                    You can sign in by google account
                </p>
            </div>

            <AuthGoogle
                title="Google"
                redirect_google={() =>
                    (window.location.href = `${BACKEND_URL}/auth/google/login`)
                }
            />


            <form onSubmit={handleSubmit(onSubmit)}>

                {type == 'register' ?
                    <input
                        placeholder="Enter your name"
                        type="text"
                        {...register('name', {
                            required: 'Enter your name'
                        })}
                    /> : ''}


                <input
                    type="email"
                    autoComplete="username"
                    placeholder="Enter your email"
                    {...register('email', {
                        required: 'Enter your email'
                    })}
                />

                <input
                    placeholder="Enter your password"
                    type="password"
                    autoComplete="current-password"
                    {...register('password', {
                        required: 'Enter your password'
                    })}
                />

                <button type="submit">{type}</button>
            </form>
        </>
    )
}