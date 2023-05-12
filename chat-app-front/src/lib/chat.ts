import { ChatProps } from "@/types/chat"


/**
 * APIから受け取ったChatデータを時系列順（降順）に整列し時期ごとに区分けする
 * 
 * カテゴリの区分けは"Today", "Yesterday", "LastWeek", "Earlier"でありChat作成日(timestamp)で区分する。
 *
 * @param {ChatProps[]} chats - APIから受け取ったChatデータ
 * @returns {[key: string]: ChatProps[]} 時期ごとに区分されたChatデータ
 */
export function sortDateChats(chats: ChatProps[]): {[key: string]: ChatProps[]} {
    const sortedChats = Array.from(chats).sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())

    const categorizedChats: {[key: string]: ChatProps[]} = {
        'Today': [],
        'Yesterday': [],
        'LastWeek': [],
        'Earlier': []
    }

    const now = new Date()

    for (const chat of sortedChats) {
        const chatDate = new Date(chat.timestamp);
        
        let category: string

        // Determine category
        if (chatDate.toDateString() === now.toDateString()) {
            category = 'Today';
        } else if (chatDate.getTime() > now.getTime() - 1 * 24 * 60 * 60 * 1000) {
            category = 'Yesterday';
        } else if (chatDate.getTime() > now.getTime() - 7 * 24 * 60 * 60 * 1000) {
            category = 'LastWeek';
        } else {
            category = 'Earlier';
        }

        categorizedChats[category]?.push(chat)
    }
    
    return categorizedChats;
}