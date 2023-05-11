import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";


const UserButton = () => {
    return (
        <section id="userButton">
            {/* User Button */}
            <div className="border-t border-white/20 pt-2">
                <div className="group relative">
                    <button className="flex w-full items-center gap-2.5 rounded-md px-3 py-3 text-sm transition-colors duration-200
                                        hover:bg-gray-800">
                        <div className="text-gray-500/80">
                            <FontAwesomeIcon icon={faUser} />
                        </div>
                        <div className="grow overflow-hidden text-ellipsis whitespace-nowrap text-left text-white">
                            User
                        </div>
                        <div className="text-gray-500/80">
                            <FontAwesomeIcon icon={faUser} />
                        </div>
                    </button>                                    
                </div>
            </div>
        </section>
    );
}

export default UserButton;