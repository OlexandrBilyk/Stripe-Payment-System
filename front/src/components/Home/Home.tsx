'use client'
import { useGetProfileQuery } from "@/redux/profileApi/profileApi"
import { useEffect } from "react"
import { useState } from "react"

export default function Home() {
    const data = useGetProfileQuery()

    useEffect(() => {
        console.log(data.currentData);
    })
 
    return <>

    </>
}