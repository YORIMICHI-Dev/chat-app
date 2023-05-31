import { useRouter } from 'next/router'
import { useContext, useEffect, useState } from 'react'
import { Context } from '@/lib/store/context'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faComment, faTrash } from '@fortawesome/free-solid-svg-icons'
import { sortDateChats } from '@/lib/chat'
import { ChatProps } from '@/types/chat'

interface Props {
    chats: { [key: string]: ChatProps[] }
}

const PastChat = ({ chats }: Props) => {
    const router = useRouter()
    const [currentChats, setCurrentChats] = useState(chats)
    const { state, dispatch } = useContext(Context)

    const routeChat = (chatId: number) => {
        dispatch({type: "SET_CHAT_ID", currentChatId: chatId})
        router.push(`/${chatId}`)
    }

    useEffect(() => {
        const fetchChats = async () => {
            // APIからすべてのChatデータを取得
            const fastAPI = process.env.NEXT_PUBLIC_API_URL
            const pastChatsResponse = await fetch(fastAPI + 'chat/all_chats')
            const pastChatsJson: ChatProps[] = await pastChatsResponse.json()

            // 時期ごとにChatデータを区分けする
            const sortedChats: { [key: string]: ChatProps[] } = sortDateChats(pastChatsJson)
            setCurrentChats(sortedChats)
        }

        fetchChats()
    }, [])


    return (
        <section
            id="pastChat"
            className="h-full transition-opacity duration-500 overflow-y-auto scrollbar-thin scrollbar-thumb-rounded hover:scrollbar-thumb-gray-500">
            <div className="flex flex-col gap-2 pb-2 text-gray-100 text-sm">
                {Object.entries(currentChats).map(([date, date_chats], id) => {
                    return (
                        date_chats.length > 0 && (
                            <div key={id}>
                                <div className="px-3 pb-2 pt-3 text-xs text-gray-500 font-medium text-ellipsis overflow-hidden break-all">
                                    {date}
                                </div>
                                <ol>
                                    {date_chats.map((chat, id) => {
                                        return chat.chat_id ===
                                            state.currentChatId ? (
                                            <li key={id}>
                                                <div className="bg-gray-800 cursor-pointer break-all rounded-md items-center relative flex p-3 gap-3">
                                                   <FontAwesomeIcon
                                                        icon={faComment}
                                                        className="h-4 w-4"
                                                    />
                                                    <div className="flex-1 text-ellipsis max-h-5 overflow-hidden break-all">
                                                        {chat.title}
                                                    </div>
                                                    <button
                                                        className="absolute flex right-1 z-10 bg-gray-800"
                                                        onClick={() =>
                                                            dispatch({
                                                                type: 'IS_OPEN_MODAL',
                                                                isOpen: true,
                                                            })
                                                        }>
                                                        <FontAwesomeIcon
                                                            icon={faTrash}
                                                            className="h-4 w-4 text-white/40 hover:text-white"
                                                        />
                                                    </button>
                                                </div>

                                            </li>
                                        ) : (
                                            <li key={id}>
                                                <div className='hover:bg-gray-800 cursor-pointer break-all rounded-md items-center relative flex p-3 gap-3'
                                                     onClick={() => routeChat(chat.chat_id)}>
                                                        <FontAwesomeIcon
                                                            icon={faComment}
                                                            className="h-4 w-4"
                                                        />
                                                        <div className="flex-1 text-ellipsis max-h-5 overflow-hidden break-all">
                                                            {chat.title}
                                                        </div>                                                
                                                </div>
                                            </li>
                                        )
                                    })}
                                </ol>
                            </div>
                        )
                    )
                })}
            </div>
        </section>
    )
}

export default PastChat
