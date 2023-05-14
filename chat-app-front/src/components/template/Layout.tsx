import Head from 'next/head'
import { ReactNode } from 'react'
import Sidebar from '../organism/Sidebar'
import Modal from '@/components/organism/Modal'
import { ChatProps } from '@/types/chat'

interface Props {
    title?: string
    chats: { [key: string]: ChatProps[] }
    currentChat: ChatProps | null
    children?: ReactNode
}

const Layout = ({
    children,
    chats,
    currentChat,
    title = 'Chat GPT Clone',
}: Props) => {
    return (
        <>
            <Head>
                <title>{title}</title>
                <meta charSet="utf-8" />
                <meta
                    name="viewport"
                    content="width=device-width,initial-scale=1.0 ,minimum-scale=1.0"
                />
                <meta name="keywords" content={title} />
                <meta name="description" content={title} />
                <meta property="og:title" content={title} />
                <meta property="og:type" content={title} />
                <meta
                    property="og:url"
                    content="https://yorimichi-chat-clone.com"
                />
                <meta property="og:image" content="画像のURL(絶対パス)" />
                <link rel="icon" href="images/favicon.ico" />
            </Head>
            <div className="overflow-hidden w-full h-full relative flex z-0">
                {currentChat !== null && (
                    <Modal />
                )}
                <Sidebar chats={chats} />
                {children}
            </div>
        </>
    )
}

export default Layout
