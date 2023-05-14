import { State, Action } from './context'

export const reducer = (state: State, action: Action) => {
    switch (action.type) {
        case 'IS_OPEN_MODAL':
            return {
                ...state,
                isModalOpen: action.isOpen,
            }

        case 'SET_CHAT_ID':
            return {
                ...state,
                currentChatId: action.currentChatId,
            }
    }
}
