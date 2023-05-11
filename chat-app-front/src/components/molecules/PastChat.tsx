import Link from "next/link";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faComment } from "@fortawesome/free-solid-svg-icons";

const PastChat = () => {
    return (
        <section id="pastChat" className="h-full transition-opacity duration-500 overflow-y-auto scrollbar-thin scrollbar-thumb-rounded hover:scrollbar-thumb-gray-500">
            <div className="flex flex-col gap-2 pb-2 text-gray-100 text-sm">
                <div className="px-3 pb-2 pt-3 text-xs text-gray-500 font-medium text-ellipsis overflow-hidden break-all">
                    Today
                </div>
                <ol>
                    <li>
                        <Link href={"/"} className="flex p-3 items-center gap-3 relative rounded-md hover:bg-gray-800 cursor-pointer break-all">
                            <FontAwesomeIcon icon={faComment} />
                            <div className="flex-1 text-ellipsis max-h-5 overflow-hidden break-all">
                                Test1 Test1 Test1 Test ssssssssssssssssssssssss
                            </div>
                        </Link>
                    </li>
                    <li>
                        <Link href={"/"} className="flex p-3 items-center gap-3 relative rounded-md hover:bg-gray-800 cursor-pointer break-all">
                            <FontAwesomeIcon icon={faComment} />
                            <div className="flex-1 text-ellipsis max-h-5 overflow-hidden break-all">
                                Test2
                            </div>
                        </Link>
                    </li>
                </ol>
            </div>
        </section>
    );
}

export default PastChat;