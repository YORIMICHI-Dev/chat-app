import { useState } from 'react'
import SettingView from '@/components/molecules/SettingView'
import CreateBox from '@/components/molecules/CreateBox'

const Main = () => {
    const [gender, setGender] = useState("female")
    const [language, setLanguage] = useState("ja")
    const [character, setCharacter] = useState("mysteriousness")
    const [gptModel, setGptModel] = useState("gpt_3_5_turbo")
    const [otherSetting, setOtherSetting] = useState("")

    return (
        <main className="w-screen h-screen">
            <div className="flex h-full max-w-full overflow-hidden relative">
                <div className="flex-grow items-stretch flex-1 overflow-auto scrollbar-thin scrollbar-thumb-rounded hover:scrollbar-thumb-gray-100">
                    <SettingView gender={gender} setGender={setGender} 
                                 language={language} setLanguage={setLanguage} 
                                 character={character} setCharacter={setCharacter}
                                 gptModel={gptModel} setGptModel={setGptModel}
                                 otherSetting={otherSetting} setOtherSetting={setOtherSetting}/>
                    <CreateBox gender={gender}
                               language={language}
                               character={character}
                               gptModel={gptModel}
                               otherSetting={otherSetting}/>
                </div>
            </div>
        </main>
    )
}

export default Main
