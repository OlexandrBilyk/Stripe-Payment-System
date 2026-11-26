import type { Cart } from "./cart"
import type { Order } from "./orders"

export type CustomerRegister = {
    name: string
    email: string
    password: string
}


export type CustomerLogin = Omit<CustomerRegister, 'name'>


export type CustomerProfile = {
    id: number,
    name: string,
    email: string,
    cart: Cart,
    orders: Order[],
}