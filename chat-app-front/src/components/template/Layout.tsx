import Head from "next/head";
import Main from "@/components/organism/Main";
import Sidebar from "@/components/organism/Sidebar";

const Layout = () => {
    return (
        <>
            <Head>
                <title>test</title>
            </Head>
            <div className="overflow-hidden w-full h-full relative flex z-0">
                <Sidebar />
                <Main />
            </div>
        </>
    );
}

export default Layout;