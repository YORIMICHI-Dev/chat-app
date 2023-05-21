import { useState, useEffect, useRef } from 'react'
import MessageBox from '@/components/molecules/MessageBox'
import SearchBox from '@/components/molecules/SearchBox'
import { ChatProps } from '@/types/chat'

interface Props {
    currentChat: ChatProps
}

const ChatView = ({ currentChat }: Props) => {
    const [chat, setChat] = useState<ChatProps>(currentChat)
    const endOfMessageRef = useRef<HTMLDivElement>(null)

    // SearchBoxに渡す、検索後に現在のchat内容を更新する関数
    const handleChatUpdate = (updatedChat: ChatProps) => {
        setChat(updatedChat)
    }

    // SearchBoxから新規の質問が発生し、Chatの内容ご更新されたとき
    useEffect(() => {
        // console.log("Chat has been updated:", chat)
        endOfMessageRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [chat])

    // PastChatから別のChat画面へ遷移したとき
    useEffect(() => {
        setChat(currentChat)
    }, [currentChat])

    return (
        <main className="w-screen h-screen">
            <div className="flex h-full max-w-full overflow-hidden relative">
                <div className="flex-grow items-stretch flex-1 overflow-auto scrollbar-thin scrollbar-thumb-rounded hover:scrollbar-thumb-gray-100">
                    <div className="flex items-center justify-center text-sm text-gray-500 p-3 border-b border-black/10">
                        Model: {chat.config.gpt.toUpperCase()}
                    </div>
                    {chat.messages.map((message, id) => {
                        return <MessageBox key={id} message={message} />
                    })}
                    <div ref={endOfMessageRef}/>
                    <div className="w-full h-32 md:h-48" />
                    <SearchBox onChatUpdate={handleChatUpdate}/>
                </div>
            </div>
        </main>
    )
}

export default ChatView
