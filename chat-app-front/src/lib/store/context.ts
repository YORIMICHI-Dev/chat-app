import { createContext, Dispatch } from 'react'

// モーダルの開閉、現在のチャットID
export type State = {
    isModalOpen: boolean
    currentChatId: number | null
}

export type Action = { type: 'IS_OPEN_MODAL'; isOpen: boolean } |
                     { type: 'SET_CHAT_ID'; currentChatId: number | null }

export const Context = createContext<{
    state: State
    dispatch: Dispatch<Action>
}>({
    state: { isModalOpen: false, currentChatId: null },
    dispatch: () => {},
})

