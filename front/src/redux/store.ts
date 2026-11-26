import { configureStore } from "@reduxjs/toolkit";
import { orderApi } from "./orderApi/orderApi";
import { authApi } from "./authApi/authApi";
import { profileApi } from "./profileApi/profileApi";
import { productApi } from "./productApi/productApi";

export const store = configureStore({
    reducer: {
        [orderApi.reducerPath]: orderApi.reducer,
        [authApi.reducerPath]: authApi.reducer,
        [profileApi.reducerPath]: profileApi.reducer,
        [productApi.reducerPath]: productApi.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware()
            .concat(orderApi.middleware)
            .concat(authApi.middleware)
            .concat(profileApi.middleware)
            .concat(productApi.middleware)
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch