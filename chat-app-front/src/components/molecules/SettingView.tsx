import ListBox from "../atom/ListBox"

interface Props {
  gender: string
  setGender: (selected: string) => void
  language: string
  setLanguage: (selected: string) => void
  character: string
  setCharacter: (selected: string) => void
  gptModel: string
  setGptModel: (selected: string) => void
  otherSetting: string
  setOtherSetting: (selected: string) => void
}

const SettingView = ({
  gender, setGender, language, setLanguage, character, setCharacter, gptModel, setGptModel, otherSetting, setOtherSetting 
}: Props) => {


    return (
        <section id="settingView">
            <div className="h-screen lg:max-w-3xl md:max-w-2xl mx-auto flex flex-col items-center justify-center space-y-10">
              <div className="text-4xl font-semibold mb-20 text-gray-400">
                Chat GPT Settings  
              </div>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-20">
                <div className="flex flex-col gap-4 items-start justify-start">
                  <span className="text-lg font-semibold text-gray-800">Gender</span>
                  <ListBox selectList={genderList} selected={gender} setSelected={setGender} />
                </div>
                <div className="flex flex-col gap-4 items-start justify-start">
                <span className="text-lg font-semibold text-gray-800">Language</span>
                  <ListBox selectList={languageList} selected={language} setSelected={setLanguage} />
                </div>
                <div className="flex flex-col gap-4 items-start justify-start">
                <span className="text-lg font-semibold text-gray-800">Character</span>
                  <ListBox selectList={characterList} selected={character} setSelected={setCharacter} />
                </div>
                <div className="flex flex-col gap-4 items-start justify-start">
                <span className="text-lg font-semibold text-gray-800">GPT Model</span>
                  <ListBox selectList={gptModelList} selected={gptModel} setSelected={setGptModel} />
                </div>
              </div>
              <div className="w-full resize-none p-4">
                <textarea
                  rows={10}
                  placeholder="Please writing more detail settings .."
                  className="w-full resize-none border-gray-300 border-2 rounded-lg  p-4 bg-transparent focus:outline-none overflow-y-hidden max-h-48"
                  value={otherSetting}
                  onChange={(e) => setOtherSetting(e.target.value)}/>                
              </div>
            </div>
        </section>
    )
}

const genderList = [
    "male",
    "female",
    "not_defined"
]

const languageList = [
    "ja",
    "en"
]

const characterList = [
    "mysteriousness",
    "elegance",
    "shyness",
    "good_taste",
    "passion",
    "maternal",
    "calm_collected",
    "sensitive",
]

const gptModelList = [
    "gpt_3_5_turbo",
]

export default SettingView
