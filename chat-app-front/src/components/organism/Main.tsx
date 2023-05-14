import SettingView from '@/components/molecules/SettingView'
import SearchBox from '@/components/molecules/SearchBox'

const Main = () => {
    return (
        <main className="w-screen h-screen">
            <div className="flex h-full max-w-full overflow-hidden relative">
                <div className="flex-grow items-stretch flex-1 overflow-auto scrollbar-thin scrollbar-thumb-rounded hover:scrollbar-thumb-gray-100">
                    <SettingView />
                    <SearchBox />
                </div>
            </div>
        </main>
    )
}

export default Main
