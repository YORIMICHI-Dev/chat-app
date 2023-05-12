import NewChatButton from "@/components/atom/NewChatButton";
import PastChat from "@/components/molecules/PastChat";
import UserButton from "@/components/atom/UserButton";
import { ChatProps } from "@/types/chat";


interface Props {
    chats: {[key: string]: ChatProps[]}
}

const Sidebar = ( {chats}: Props) => {
    return (
        <nav className="bg-gray-900 flex-shrink-0 overflow-x-hidden h-screen md:block hidden">
            <div className="flex h-full w-hull flex-col p-2 w-[260px]">
                <NewChatButton />
                <PastChat chats={chats}/>
                <UserButton />
            </div>
        </nav>
    );
}

export default Sidebar;