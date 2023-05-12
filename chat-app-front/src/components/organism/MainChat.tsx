import MessageBox from "../molecules/MessageBox";
import SearchBox from "@/components/molecules/SearchBox";
import { ChatProps } from "@/types/chat";


interface Props {
    chat: ChatProps
}


const MainChat = ({chat}: Props) => {
    return (
        <main className="w-screen h-screen">
            <div className="flex h-full max-w-full overflow-hidden">
                <div className="relative h-full w-full flex flex-col overflow-hidden items-stretch flex-1">
                    {chat.messages.map((message, id) => {
                        return (
                            <MessageBox key={id} message={message} />                            
                        )
                    })}

                    <SearchBox />
                </div>
            </div>

        </main>
    );
}

export default MainChat;