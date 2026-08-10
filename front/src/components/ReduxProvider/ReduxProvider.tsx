'use client'
import { Provider } from "react-redux"
import { store } from "@/redux/store"
import Root from "react"

type ReduxProviderProps = {
    children: Root.ReactNode
}

export default function ReduxProvider({ children }: ReduxProviderProps) {
    return (
        <Provider store={store}>
            {children}
        </Provider>
    )
}