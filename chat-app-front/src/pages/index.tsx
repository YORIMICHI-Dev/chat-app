import Layout from "@/components/template/Layout"
import Main from "@/components/organism/Main"
import { ChatProps } from "@/types/chat"
import { sortDateChats } from "@/lib/chat"


interface Props {
    chats: {[key: string]: ChatProps[]}
}


export default function Home( {chats}: Props) {

    return (
        <>
            <Layout chats={chats}>
                <Main />
            </Layout>
        </>
    )
}


export const getServerSideProps = async() => {
    // APIからすべてのChatデータを取得
    const fastAPI = process.env.API_URL
    const pastChatsResponse = await fetch(fastAPI + "/chat/all_chats")
    const pastChatsJson = await pastChatsResponse.json()

    // 時期ごとにChatデータを区分けする
    const sortedChats: {[key: string]: ChatProps[]} = sortDateChats(pastChatsJson)

    return {
        props: {
            chats: sortedChats
        }
    }
}