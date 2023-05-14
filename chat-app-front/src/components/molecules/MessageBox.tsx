import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUser, faRobot } from '@fortawesome/free-solid-svg-icons'
import { MessageProps } from '@/types/chat'

interface Props {
    message: MessageProps
}

const MessageBox = ({ message }: Props) => {
    return (
        <section id="messageBox">
            <div className="h-full overflow-hidden first-letter:flex flex-col items-center">
                <div className="group w-full text-gray-800 border-b border-black/10">
                    <div className="flex p-4 gap-4 text-base md:gap-6 md:max-w-2xl lg:max-w-3xl md:py-6 lg:px-0 m-auto">
                        <div className="flex-shrink-0 flex flex-col relative items-end">
                            {message.role === 'assistant' ? (
                                <FontAwesomeIcon
                                    icon={faRobot}
                                    className="h-6 w-6 text-blue-500"
                                />
                            ) : (
                                <FontAwesomeIcon
                                    icon={faUser}
                                    className="h-6 w-6 text-red-500"
                                />
                            )}
                        </div>
                        <div>{message.content}</div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default MessageBox
