import MessageBox from '@/components/molecules/MessageBox'
import SearchBox from '@/components/molecules/SearchBox'
import { ChatProps } from '@/types/chat'

interface Props {
    currentChat: ChatProps
}

const ChatView = ({ currentChat }: Props) => {
    return (
        <main className="w-screen h-screen">
            <div className="flex h-full max-w-full overflow-hidden relative">
                <div className="flex-grow items-stretch flex-1 overflow-auto scrollbar-thin scrollbar-thumb-rounded hover:scrollbar-thumb-gray-100">
                    <div className="flex items-center justify-center text-sm text-gray-500 p-3 border-b border-black/10">
                        Model: {currentChat.config.gpt.toUpperCase()}
                    </div>
                    {currentChat.messages.map((message, id) => {
                        return <MessageBox key={id} message={message} />
                    })}
                    <div className="w-full h-32 md:h-48" />
                    <SearchBox />
                </div>
            </div>
        </main>
    )
}

export default ChatView
