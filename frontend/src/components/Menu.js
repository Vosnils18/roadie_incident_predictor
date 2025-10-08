import React from "react";
import { useNavigate } from "react-router-dom";
import { signOut } from "firebase/auth"; // Import the signOut function
import { auth } from "../api/firebaseConfig"; // Import the auth instance
import Cookies from "js-cookie"; // Import js-cookie library


// Assets
import { ReactComponent as CloseIcon } from '../assets/icons/close.svg';
import { ReactComponent as HomeIcon } from '../assets/icons/house.svg';
import { ReactComponent as StatIcon } from '../assets/icons/chart-area.svg';
import { ReactComponent as UserIcon } from '../assets/icons/user.svg';
import { ReactComponent as SubIcon } from '../assets/icons/subscription.svg';
import { ReactComponent as Logo } from '../assets/icons/logo.svg';

// Components
import { MenuButton, Button, Button2 } from "./Buttons";

const Menu = ({ action, isMenuOpen }) => {
    const navigate = useNavigate();

    const handleLogout = async () => {
    
        try {
            await signOut(auth); // Call the signOut function
            Cookies.remove('mode'); // Remove the 'mode' cookie
            navigate('/auth'); // Redirect to the login page
        } catch (error) {
            console.error('Error logging out:', error);
        }
    };

    return (
        <div className={`bg-cyan-950 w-full h-full fixed p-5 transform ${isMenuOpen ? 'translate-x-0' : '-translate-x-full'} transition-all ease-in-out z-100`}>
            <div className="flex justify-between items-center">
                <div className="flex gap-5 justify-center items-center">
                    <Logo ></Logo>
                    <h1 className="text-3xl font-bold text-white">Roadie</h1>
                </div>
                <CloseIcon className="h-7 w-7 fill-white active:fill-cyan-300 " onClick={action} />
            </div>
            <div className="mt-10 flex flex-col gap-3 relative h-full">
                <MenuButton title={'Dashboard'} url={'/'} icon={<HomeIcon />} active></MenuButton>
                <MenuButton title={'Statistics'} url={'/statistics'} icon={<StatIcon />} ></MenuButton>
                <MenuButton title={'Profile'} url={'/profile'} icon={<UserIcon />} ></MenuButton>
                <MenuButton title={'Subscriptions'} url={'/subscriptions'} icon={<SubIcon />} ></MenuButton>

                <div className="absolute bottom-20 w-full gap-4 flex flex-col">
                    <Button2 title={'Change Mode'} action={() => {navigate('/mode')}}></Button2>
                    <Button title={'Logout'} action={handleLogout}></Button>
                </div>
            </div>
        </div>
    );
};

export default Menu;
