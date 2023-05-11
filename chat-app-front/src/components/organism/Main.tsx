import ChatBox from "../molecules/ChatBox";
import SearchBox from "@/components/molecules/SearchBox";


const Main = () => {
    return (
        <main className="w-screen h-screen">
            <div className="flex h-full max-w-full overflow-hidden">
                <div className="relative h-full w-full flex flex-col overflow-hidden items-stretch flex-1">
                    <ChatBox />
                    <SearchBox />
                </div>
            </div>

        </main>
    );
}

export default Main;