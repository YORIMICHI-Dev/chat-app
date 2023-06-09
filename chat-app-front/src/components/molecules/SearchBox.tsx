import { useState, useContext } from 'react'
import { Context } from '@/lib/store/context'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faRefresh, faPaperPlane } from '@fortawesome/free-solid-svg-icons'
import { ChatProps } from '@/types/chat'

interface Props {
    onChatUpdate: (updatedChat: ChatProps) => void
}

const SearchBox = ({onChatUpdate}: Props) => {
    const {state, dispatch} = useContext(Context)
    const [content, setContent] = useState<string>('')

    const sendRequest = async (e: React.MouseEvent) => {
        // リダイレクト防止
        e.preventDefault()

        try {
            // 入力がない場合は処理せず
            if (content === ''.trim()) {
                    console.log('No Input')
            } else {
                const jsonString = JSON.stringify({
                    content: content,
                })
                const request = {
                    method: 'POST',
                    headers: new Headers({
                        'Content-Type': 'application/json',
                    }),
                    body: jsonString,
                }

                const response = await fetch(
                    process.env.NEXT_PUBLIC_API_URL +
                        'chat/add_chat/' +
                        `${state.currentChatId}`,
                    request
                )
                const json = await response.json()

                if (response.ok) {
                    // 現在のChatViewに対して、返信後のChatを更新する
                    const response = await fetch(
                        process.env.NEXT_PUBLIC_API_URL +
                            "chat/get_chat/" +
                            `${state.currentChatId}`
                    )
                    const json = await response.json()
                    onChatUpdate(json)
                }
                setContent('')
            } 
        } catch (error) {
            console.error('Error Create Post: ', error)
        }
    }

    return (
        <section
            id="searchBox"
            className="w-full absolute bottom-10 left-1/2 -translate-x-1/2">
            <div className="w-full h-full border-t md:border-t-0 md:border-transparent">
                <form className="flex flex-row-reverse items-center md:flex-col md:mx-4 lg:mx-auto lg:max-w-2xl pt-2">
                    {/* Regenerate未実装 */}
                    {/* <div className="h-full flex ml-1 md:w-full md:m-auto md:mb-2 gap-0 md:gap-2 justify-center">
                        <button className="md:border p-2 hover:bg-gray-100 rounded-md bg-white">
                            <div className="flex w-full gap-2 items-center justify-center">
                                <FontAwesomeIcon
                                    icon={faRefresh}
                                    className="h-4 w-4"
                                />
                                <span className="hidden md:block">
                                    Regenerate response
                                </span>
                            </div>
                        </button>
                    </div> */}
                    <div className="relative flex flex-col w-full py-2 flex-grow md:py-3 md:pl-4 border border-black/10 bg-white dark:border-gray-900/50 dark:text-white dark-bg-gray-700 rounded-md shadow-md">
                        <textarea
                            rows={1}
                            placeholder="Send a message."
                            className="m-0 w-full resize-none border-0 bg-transparent p-0 pr-7 focus:outline-none pl-2 md:pl-0 overflow-y-hidden max-h-48"
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                        />
                        <button
                            className="absolute p-1 rounded-md text-gray-500 bottom-1.5 md:bottom-2.5 hover:bg-gray-100 right-1 md:right-2"
                            onClick={sendRequest}>
                            <FontAwesomeIcon
                                icon={faPaperPlane}
                                className="h-4 w-4"
                            />
                        </button>
                    </div>
                </form>
            </div>
        </section>
    )
}
export default SearchBox
