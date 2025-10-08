import React, { useState, useEffect } from "react";
import Cookies from "js-cookie"; // Import js-cookie library
import { useNavigate } from "react-router-dom";

// Components
import LoadingSpinner from "../components/Loader";
import { ColoredTitle, TitleWithSubtitle } from "../components/Titles";

// Assets
import DemoImage from '../assets/images/test.svg';
import LiveImage from '../assets/images/live.svg';
import { Button, Button2 } from "../components/Buttons";
import Gap from "../components/Gap";

const Mode = () => {
    const navigate = useNavigate();
    // State for loading
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setLoading(false);
        }, 1000); // Simulate a 2 second loading time

        return () => clearTimeout(timer);
    }, []);

    const handleDemoMode = () => {
        Cookies.set('mode', 'demo', { expires: 7 }); // Set cookie for demo mode with 7 days expiration
        console.log('Demo mode activated');
        navigate('/'); // Redirect to the homepage
    };

    const handleLiveMode = () => {
        Cookies.set('mode', 'live', { expires: 7 }); // Set cookie for live mode with 7 days expiration
        console.log('Live mode activated');
        navigate('/'); // Redirect to the homepage
    };

    const titleSegments = [
        { text: 'Choose ', colorClass: 'text-gray-800' },
        { text: 'Demo', colorClass: 'text-emerald-500' },
        { text: ' or ', colorClass: 'text-gray-800' },
        { text: 'Live', colorClass: 'text-emerald-500' },
        { text: ' - We Have Got', colorClass: 'text-gray-800' },
        { text: ' You Covered!', colorClass: 'text-emerald-500' }
    ];

    return (
        <div className="w-screen h-screen">
            {loading ? (
                <div className="w-full h-full flex justify-center items-center">
                    <LoadingSpinner />
                </div>
            ) : (
                <div className="p-5 bg-white h-fill lg:h-full">
                    <div className="max-w-screen-lg mx-auto">
                        <ColoredTitle segments={titleSegments} subtitle="Select wether you would like to use your data, or our test data." />
                    </div>

                    <div className="flex flex-col lg:flex-row gap-4 mt-10 lg:w-9/12 lg:mx-auto">
                        <div className="bg-gray-100 p-5 rounded-xl lg:flex-1">
                            <img src={DemoImage} className="p-10 lg:h-96" alt="Demo" />
                            <TitleWithSubtitle 
                                    title="Demo"
                                    subtitle="Use dummy data to try out the functions and features"
                                    color={2} // Change this value to 1 or 2 to test different color schemes
                            />
                            <Gap></Gap>
                            <Button2 title="Use Demo Data" action={handleDemoMode} />
                        </div>

                        <div className="bg-cyan-950 p-5 rounded-xl lg:flex-1">
                            <img src={LiveImage} className="p-10  lg:h-96" alt="Live" />
                            <TitleWithSubtitle title="Live" subtitle="Use your location, speed for the predictions!" />
                            <Gap></Gap>
                            <Button title="Use Live Data (coming soon)"  />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Mode;
