export type CustomerRegister = {
    name: string
    email: string
    password: string
}

export type CustomerLogin = Omit<CustomerRegister, 'name'>

