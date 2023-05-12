import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import Image from "next/image";
import img from "/public/images/icon.png"

const UserButton = () => {
    return (
        <section id="userButton">
            {/* User Button */}
            <div className="border-t border-white/20 pt-2">
                <div className="group relative">
                    <button className="flex w-full items-center gap-2.5 rounded-md px-3 py-3 text-sm transition-colors duration-200
                                        hover:bg-gray-800">
                        <div className="">
                            <Image src={img} alt="no image" width={20}/>
                        </div>
                        <div className="grow overflow-hidden text-ellipsis whitespace-nowrap text-left text-white">
                            User
                        </div>
                        <div className="text-gray-500/80">
                            <FontAwesomeIcon icon={faBars} className="h-4 w-4" />
                        </div>
                    </button>                                    
                </div>
            </div>
        </section>
    );
}

export default UserButton;