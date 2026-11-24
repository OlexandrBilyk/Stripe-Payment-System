import { FaGoogle } from 'react-icons/fa';

type AuthGoogleProps = {
    redirect_google: () => void,
    title: string
}

export default function AuthGoogle({ redirect_google, title }: AuthGoogleProps) {

    return <>
        <button type="button" onClick={redirect_google}>
            <FaGoogle></FaGoogle>
            {title}
        </button>
    </>
}