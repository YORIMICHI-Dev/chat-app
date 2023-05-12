import Head from "next/head";
import Sidebar from "@/components/organism/Sidebar";
import Main from "@/components/organism/Main";
import { ChatProps } from "@/types/chat"
import { ReactNode } from "react";


interface Props {
    chats: {[key: string]: ChatProps[]}
    children?: ReactNode
}


const Layout = ({chats, children}: Props) => {
    return (
        <>
            <Head>
                <title>Chat GPT Clone</title>
                <meta charSet="utf-8" />
                <meta name="viewport" content="width=device-width,initial-scale=1.0 ,minimum-scale=1.0" />
                <meta name="keywords" content={"Chat GPT"} />
                <meta name="description" content={"Chat GPT Clone"} />
                <meta property="og:title" content={"Chat GPT Clone"} />
                <meta property="og:type" content={"website"} />
                <meta property="og:url" content="https://yorimichi-chat-clone.com" />
                <meta property="og:image" content="画像のURL(絶対パス)" />
                <link rel="icon" href="images/favicon.ico" />
            </Head>
            <div className="overflow-hidden w-full h-full relative flex z-0">
                <Sidebar chats={chats} />
                {children}
            </div>
        </>
    );
}

export default Layout;