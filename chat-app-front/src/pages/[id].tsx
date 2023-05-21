import Layout from '@/components/template/Layout'
import ChatView from '@/components/organism/ChatView'
import { ChatProps } from '@/types/chat'
import { sortDateChats } from '@/lib/chat'
import { GetStaticPropsContext } from 'next'
import { useEffect, useContext } from 'react'
import { Context } from '@/lib/store/context'

interface Props {
    chats: { [key: string]: ChatProps[] }
    currentChat: ChatProps
    currentChatTitle: string
}

export default function ChatPage({ chats, currentChat }: Props) {
    const {state, dispatch} = useContext(Context)

    useEffect(() => {
        dispatch({type: "SET_CHAT_ID", currentChatId: currentChat.chat_id})            
    }, [dispatch, currentChat])

    return (
        <>
            <Layout
                chats={chats}
                currentChat={currentChat}
                title={currentChat.title}>
                <ChatView currentChat={currentChat} />
            </Layout>
        </>
    )
}

export const getStaticPaths = async () => {
    try {
        // APIからすべてのChatデータを取得
        const fastAPI = process.env.NEXT_PUBLIC_API_URL
        const pastChatsResponse = await fetch(fastAPI + 'chat/all_chats')
        const pastChatsJson: ChatProps[] = await pastChatsResponse.json()

        const paths = pastChatsJson.map((chat) => {
            return {
                params: { id: chat.chat_id.toString() },
            }
        })

        return {
            paths: paths,
            fallback: true,
        }
    } catch (error) {
        console.error('Error getting chat on getStaticPaths: ', error)
    }
}

export const getStaticProps = async (context: GetStaticPropsContext) => {
    const id = context.params?.id

    try {
        // APIからすべてと特定のChatデータを取得
        const fastAPI = process.env.NEXT_PUBLIC_API_URL

        const pastChatsResponse = await fetch(fastAPI + 'chat/all_chats')
        const pastChatsJson = await pastChatsResponse.json()
        // 時期ごとにChatデータを区分けする
        const sortedChats: { [key: string]: ChatProps[] } =
            sortDateChats(pastChatsJson)

        const selectChatResponse = await fetch(fastAPI + `chat/get_chat/${id}`)
        const selectChatJson: ChatProps = await selectChatResponse.json()

        return {
            props: {
                chats: sortedChats,
                currentChat: selectChatJson,
            },
        }
    } catch (error) {
        console.error('Error getting chat: ', error)
    }
}
