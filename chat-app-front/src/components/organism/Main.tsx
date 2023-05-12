import ChatBox from "../molecules/MessageBox";
import SearchBox from "@/components/molecules/SearchBox";
import { ChatProps } from "@/types/chat";


const Main = () => {
    return (
        <main className="w-screen h-screen">
            <div className="flex h-full max-w-full overflow-hidden">
                <div className="relative h-full w-full flex flex-col overflow-hidden items-stretch flex-1">
                    {/* <ChatBox chat={chat} /> */}
                    <SearchBox />
                </div>
            </div>

        </main>
    );
}

export default Main;