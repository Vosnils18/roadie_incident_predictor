import React, { useEffect, useState } from "react";
import { ReactComponent as MenuIcon } from '../assets/icons/menu.svg';
import { ReactComponent as NotificationIcon } from '../assets/icons/notification.svg';
import { auth } from "../api/firebaseConfig"; // Import Firebase auth
import { signOut } from "firebase/auth"; // Import the signOut function
import Cookies from "js-cookie"; // Import js-cookie library
import { useNavigate } from "react-router-dom";

const Navbar = ({ action }) => {
    const [userProfile, setUserProfile] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        // Fetch user profile data when the component mounts
        const fetchUserProfile = async () => {
            try {
                const user = auth.currentUser;
                if (user) {
                    // Use the user's display name and photo URL
                    setUserProfile({
                        displayName: user.displayName,
                        photoURL: user.photoURL
                    });
                }
            } catch (error) {
                console.error("Error fetching user profile:", error);
            }
        };

        fetchUserProfile();

        // Cleanup function
        return () => setUserProfile(null);
    }, []);

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
        <div className="bg-cyan-950 fixed h-16 flex justify-between p-5 items-center transition-all w-full max-w-screen-xl mx-auto rounded-b-lg mt-0 lg:mt-1 lg:rounded-lg">
            <div className="lg:hidden">
                <MenuIcon className="h-5 w-5 fill-white active:fill-cyan-300 hover:fill-cyan-300" onClick={action} />
            </div>
            <div className="hidden lg:flex items-center justify-between w-full text-white">
                <h1 className="text-3xl font-bold text-white">Roadie</h1>
                <div className="flex gap-5 mr-10 pr-10 border-r-2">
                    <a href="/">
                        <h1 className="font-bold capitalize hover:bg-cyan-900 p-2 transition-all rounded-md cursor-pointer">Dashboard</h1>
                    </a>
                    <a href="/statistics">
                        <h1 className="font-bold capitalize hover:bg-cyan-900 p-2 transition-all rounded-md cursor-pointer">Statistics</h1>
                    </a>
                    <a href="/subscriptions">
                        <h1 className="font-bold capitalize hover:bg-cyan-900 p-2 transition-all rounded-md cursor-pointer">Subscriptions</h1>
                    </a>
                    <a href="/mode">
                        <h1 className="font-bold capitalize hover:bg-cyan-900 p-2 transition-all rounded-md cursor-pointer">Mode</h1>
                    </a>
                    <a href="/tutorial">
                        <h1 className="font-bold capitalize hover:bg-cyan-900 p-2 transition-all rounded-md cursor-pointer">Tutorial</h1>
                    </a>
                    <h1 className="font-bold capitalize hover:text-red-600 p-2 transition-all rounded-md cursor-pointer" onClick={handleLogout}>Logout</h1>
                </div>
            </div>
            <div className="flex gap-4 items-center">
                <div className="relative">
                    <a href='/notifications'>
                        <NotificationIcon className="h-5 w-5 fill-white active:fill-cyan-300 hover:fill-cyan-300" />
                    </a>
                </div>
                <div className="h-8 w-8 bg-white rounded-full flex items-center justify-center overflow-hidden">
                    <a href="/profile">
                        {userProfile ? (
                            <img src={userProfile.photoURL} alt="User profile" className="h-full w-full rounded-full" />
                        ) : (
                            <div className="h-full w-full rounded-full bg-white"></div>
                        )}
                    </a>
                </div>
            </div>
        </div>
    );
};

export default Navbar;
