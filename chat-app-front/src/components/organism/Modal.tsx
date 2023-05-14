import { Dialog, Transition } from '@headlessui/react'
import { Fragment, useContext } from 'react'
import { useRouter } from 'next/router'
import { Context } from '@/lib/store/context'


const Modal = () => {
    const router = useRouter()
    const { state, dispatch } = useContext(Context)

    const deleteChat = async (e: React.MouseEvent) => {
        e.preventDefault()

        try {
            const response = await fetch(
                process.env.NEXT_PUBLIC_API_URL +
                    `chat/delete_chat/${state.currentChatId}`,
                { method: 'DELETE' }
            )
            const json = await response.json()

            if (response.ok) {
                dispatch({ type: 'IS_OPEN_MODAL', isOpen: false })
                router.push('/')
            } else {
                throw json
            }
        } catch (error) {
            console.error('Error deleting chat: ', error)
        }
    }

    return (
        <Transition appear show={state.isModalOpen} as={Fragment}>
            <Dialog
                as="div"
                className="relative z-10"
                onClose={() =>
                    dispatch({ type: 'IS_OPEN_MODAL', isOpen: false })
                }>
                {/* Background */}
                <Transition.Child
                    as={Fragment}
                    enter="ease-out duration-300"
                    enterFrom="opacity-0"
                    enterTo="opacity-100"
                    leave="ease-in duration-200"
                    leaveFrom="opacity-100"
                    leaveTo="opacity-0">
                    <div className="fixed inset-0 bg-black bg-opacity-25" />
                </Transition.Child>

                {/* Modal */}
                <div className="fixed inset-0 overflow-y-auto">
                    <div className="flex min-h-full items-center justify-center p-4 text-center">
                        <Transition.Child
                            as={Fragment}
                            enter="ease-out duration-300"
                            enterFrom="opacity-0 scale-95"
                            enterTo="opacity-100 scale-100"
                            leave="ease-in duration-200"
                            leaveFrom="opacity-100 scale-100"
                            leaveTo="opacity-0 scale-95">
                            <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                                <Dialog.Title
                                    as="h3"
                                    className="text-lg font-medium leading-6 text-gray-900">
                                    Notification!
                                </Dialog.Title>
                                <div className="mt-2">
                                    <p className="text-gray-500">
                                        Do you want to Delete Chat?
                                    </p>
                                </div>

                                <div className="mt-4 flex justify-between">
                                    <button
                                        type="button"
                                        className="inline-flex justify-center rounded-md border border-transparent bg-red-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-red-200"
                                        onClick={(e) => deleteChat(e)}>
                                        Yes Delete
                                    </button>
                                    <button
                                        type="button"
                                        className="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200"
                                        onClick={() =>
                                            dispatch({
                                                type: 'IS_OPEN_MODAL',
                                                isOpen: false,
                                            })
                                        }>
                                        No
                                    </button>
                                </div>
                            </Dialog.Panel>
                        </Transition.Child>
                    </div>
                </div>
            </Dialog>
        </Transition>
    )
}

export default Modal
