export interface SystemProps {
    id: number
    chat_id: number
    gender: string
    language: string
    character: string
    other_setting?: string
}

export interface MessageProps {
    id: number
    chat_id: number
    role: string
    content: string
    timestamp: string
}

export interface ConfigProps {
    id: number
    chat_id: number
    gpt: string
    max_tokens: number
    temperature: number
}

export interface ChatProps {
    chat_id: number
    timestamp: string
    title: string
    system: SystemProps
    config: ConfigProps
    messages: MessageProps[]
}
