import Layout from '@/components/template/Layout'
import Main from '@/components/organism/Main'
import { ChatProps } from '@/types/chat'
import { sortDateChats } from '@/lib/chat'
import { Context } from '@/lib/store/context'
import { useContext, useEffect } from 'react'

interface Props {
    chats: { [key: string]: ChatProps[] }
}

export default function Home({ chats }: Props) {
    const {state, dispatch} = useContext(Context)

    useEffect(() => {
        dispatch({type: "SET_CHAT_ID", currentChatId: null})            
    }, [dispatch])

    return (
        <>
            <Layout chats={chats} currentChat={null}>
                <Main />
            </Layout>
        </>
    )
}

export const getStaticProps = async () => {
    // APIからすべてのChatデータを取得
    const fastAPI = process.env.NEXT_PUBLIC_API_URL
    const pastChatsResponse = await fetch(fastAPI + 'chat/all_chats')
    const pastChatsJson: ChatProps[] = await pastChatsResponse.json()

    // 時期ごとにChatデータを区分けする
    const sortedChats: { [key: string]: ChatProps[] } =
        sortDateChats(pastChatsJson)

    return {
        props: {
            chats: sortedChats,
        },
    }
}
