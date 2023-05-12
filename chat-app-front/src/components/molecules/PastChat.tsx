import Link from "next/link";
import { ChatProps } from "@/types/chat";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faComment } from "@fortawesome/free-solid-svg-icons";


interface Props {
    chats: {[key: string]: ChatProps[]}
}


const PastChat = ({chats}: Props) => {
    
    return (
        <section id="pastChat" className="h-full transition-opacity duration-500 overflow-y-auto scrollbar-thin scrollbar-thumb-rounded hover:scrollbar-thumb-gray-500">
            <div className="flex flex-col gap-2 pb-2 text-gray-100 text-sm">
                {Object.entries(chats).map(([date, date_chats], id) => {
                    return date_chats.length > 0 && (
                        <div key={id}>
                            <div className="px-3 pb-2 pt-3 text-xs text-gray-500 font-medium text-ellipsis overflow-hidden break-all">
                                {date}
                            </div>
                            <ol>
                                {date_chats.map((chat, id) => {
                                    
                                    return(
                                        <li key={id}>
                                            <Link href={`/${chat.chat_id}`} className="flex p-3 items-center gap-3 relative rounded-md hover:bg-gray-800 cursor-pointer break-all">
                                                <FontAwesomeIcon icon={faComment} className="h-4 w-4" />
                                                <div className="flex-1 text-ellipsis max-h-5 overflow-hidden break-all">
                                                    {chat.title}
                                                </div>                                                    
                                            </Link>
                                        </li>
                                    )
                                })}
                            </ol>
                        </div>
                    )
                })}
            </div>
        </section>
    );
}

export default PastChat;