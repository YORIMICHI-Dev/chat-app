import Link from 'next/link'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus } from '@fortawesome/free-solid-svg-icons'

const NewChatButton = () => {
    return (
        <section id="newChatButton">
            <Link
                href={'/'}
                className="flex py-3 px-3 items-center gap-3 transition-colors duration-200 text-white cursor-pointer text-sm rounded-md 
                            border border-white/20 hover:bg-gray-500/10 mb-1 flex-shrink-0 ">
                <FontAwesomeIcon icon={faPlus} className="h-4 w-4" />
                <span>New chat</span>
            </Link>
        </section>
    )
}

export default NewChatButton
