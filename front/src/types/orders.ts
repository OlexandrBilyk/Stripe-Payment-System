import type { Product } from "./product"

export type OrderItem = {
    id: number, 
    order_id: number, 
    product: Product,
    quantity: number, 
    price: number,
}


export type Payment = {
    id: number, 
    stripe_id: string,
    status: string,
    order_id: number,
}


export type Order = {
    id: number, 
    status: string,
    order_items: OrderItem[],
    payments: Payment[],
}

