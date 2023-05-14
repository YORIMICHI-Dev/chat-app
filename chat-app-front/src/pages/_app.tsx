import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import { useReducer } from 'react'
import { Context, State } from '@/lib/store/context'
import { reducer } from '@/lib/store/reducer'

export default function App({ Component, pageProps }: AppProps) {
    const contextState: State = { isModalOpen: false, currentChatId: null }
    const [state, dispatch] = useReducer(reducer, contextState)

    return (
        <Context.Provider value={{ state, dispatch }}>
            <Component {...pageProps} />
        </Context.Provider>
    )
}
