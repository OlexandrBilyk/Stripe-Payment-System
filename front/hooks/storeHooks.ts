import type { TypedUseSelectorHook } from "react-redux";
import { useDispatch, UseDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "@/redux/store";


export const useTypificatedSelector: TypedUseSelectorHook<RootState> = useSelector
export const useTypificatedDispatch = useDispatch<AppDispatch>()