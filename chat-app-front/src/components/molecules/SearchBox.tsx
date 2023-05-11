import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRefresh, faPaperPlane } from "@fortawesome/free-solid-svg-icons";


const SearchBox = () => {
    return (
        <section id="searchBox" className="w-full absolute bottom-10 left-0 ">
            <div className="w-full h-full border-t md:border-t-0 md:border-transparent">
                <form className="flex flex-row-reverse items-center md:flex-col md:mx-4 lg:mx-auto lg:max-w-2xl pt-2">
                    <div className="h-full flex ml-1 md:w-full md:m-auto md:mb-2 gap-0 md:gap-2 justify-center">
                        <button className="md:border p-2 hover:bg-gray-100 rounded-md">
                            <div className="flex w-full gap-2 items-center justify-center">
                                <FontAwesomeIcon icon={faRefresh} />
                                <span className="hidden md:block">Regenerate response</span>
                            </div>
                        </button>
                    </div>
                    <div className="relative flex flex-col w-full py-2 flex-grow md:py-3 md:pl-4 border border-black/10 bg-white dark:border-gray-900/50 dark:text-white dark-bg-gray-700 rounded-md shadow-md">
                        <textarea rows={1} placeholder="Send a message." className="m-0 w-full resize-none border-0 bg-transparent p-0 pr-7 focus:outline-none pl-2 md:pl-0 overflow-y-hidden"/>
                        <button className="absolute p-1 rounded-md text-gray-500 bottom-1.5 md:bottom-2.5 hover:bg-gray-100 right-1 md:right-2">
                            <FontAwesomeIcon icon={faPaperPlane} />
                        </button>
                    </div>
                </form>                
            </div>
        </section>
    );
}

export default SearchBox;