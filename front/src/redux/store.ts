import { configureStore } from "@reduxjs/toolkit";
import { orderApi } from "./orderApi/orderApi";
import { authApi } from "./authApi/authApi";
import { profileApi } from "./profileApi/profileApi";

export const store = configureStore({
    reducer: {
        [orderApi.reducerPath]: orderApi.reducer,
        [authApi.reducerPath]: authApi.reducer,
        [profileApi.reducerPath]: profileApi.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware()
            .concat(orderApi.middleware)
            .concat(authApi.middleware)
            .concat(profileApi.middleware)
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch