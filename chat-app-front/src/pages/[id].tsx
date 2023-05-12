import Layout from "@/components/template/Layout";
import MainChat from "@/components/organism/MainChat";
import { ChatProps } from "@/types/chat";
import { sortDateChats } from "@/lib/chat";


interface Props {
    chats: {[key: string]: ChatProps[]}
    chat: ChatProps
}


export default function ChatPage({chats, chat}: Props) {

    return (
        <>
            <Layout chats={chats}>
                <MainChat chat={chat} />
            </Layout>
        </>
    )
}


export const getStaticPaths = async() => {
    // APIからすべてのChatデータを取得
    const fastAPI = process.env.API_URL
    const pastChatsResponse = await fetch(fastAPI + "/chat/all_chats")
    const pastChatsJson: ChatProps[] = await pastChatsResponse.json()

    const paths = pastChatsJson.map((chat) => {
        return {
            params: { id: chat.chat_id.toString() }
        }
    })

    return {
        paths: paths,
        fallback: true,
    }
}


export const getStaticProps = async({ params }) => {
    const { id } = params

    // APIからすべてと特定のChatデータを取得
    const fastAPI = process.env.API_URL

    const pastChatsResponse = await fetch(fastAPI + "/chat/all_chats")
    const pastChatsJson = await pastChatsResponse.json()
    // 時期ごとにChatデータを区分けする
    const sortedChats: {[key: string]: ChatProps[]} = sortDateChats(pastChatsJson)

    const selectChatResponse = await fetch(fastAPI + `/chat/get_chat/${id}`)
    const selectChatJson = await selectChatResponse.json()

    return {
        props: {
            chats: sortedChats,
            chat: selectChatJson,
        }
    }
}