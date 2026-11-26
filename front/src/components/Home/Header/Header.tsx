'use client'

import { useGetProfileQuery } from "@/redux/profileApi/profileApi"
import { useRouter } from "next/navigation"

export default function Header() {
    const { data } = useGetProfileQuery()
    const router = useRouter()

    const handleProfile = function () {
        router.push('/profile')
    }

    const handleCart = function () {
        router.push('/cart')
    }



    return (
        <header>
            <nav>
                <ul>
                    <li>
                        <button type="button" onClick={handleCart}>
                            Cart
                        </button>
                    </li>
                    <li>History</li>
                </ul>
            </nav>
            <div>
                <button type="button" onClick={handleProfile}>
                    {data?.email[0]}
                </button>
            </div>

        </header>
    )
}