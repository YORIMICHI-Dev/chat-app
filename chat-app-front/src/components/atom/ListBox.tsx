import { Fragment } from "react"
import { Listbox, Transition } from "@headlessui/react"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faUpDown, faCheck } from "@fortawesome/free-solid-svg-icons"

interface Props {
    selectList: string[]
    selected: string
    setSelected: (selected: string) => void
}

function ListBox({selectList, selected, setSelected}: Props) {
    return (
        <div className="w-40">
            <Listbox value={selected} onChange={setSelected}>
                <div className="relative mt-1">
                    <Listbox.Button className="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm">
                        <span className="block truncate">{selected}</span>
                        <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                            <FontAwesomeIcon icon={faUpDown} className="h-5 w-5 text-gray-300" />
                        </span>
                    </Listbox.Button>
                    <Transition
                        as={Fragment}
                        leave="transition ease-in duration-100"
                        leaveFrom="opacity-100"
                        leaveTo="opacity-0">
                        <Listbox.Options className="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                        {selectList.map((select, selectId) => (
                            <Listbox.Option 
                            key={selectId} 
                            className={({ active }) => `relative cursor-default select-none py-2 pl-10 pr-4 ${active ? 'bg-amber-100 text-amber-900' : 'text-gray-900'}`}
                            value={select}>
                            {({ selected }) => (
                                <>
                                    <span className={`block truncate ${ selected ? 'font-medium' : 'font-normal' }`}>
                                        {select}
                                    </span>
                                    {selected ? (
                                        <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-amber-600">
                                            <FontAwesomeIcon icon={faCheck} className="h-5 w-5" />
                                        </span>
                                    ) : null}                                
                                </>
                            )}
                            </Listbox.Option>
                        ))}
                        </Listbox.Options>
                    </Transition>
                    </div>
                </Listbox>
        </div>
    );
}

export default ListBox;