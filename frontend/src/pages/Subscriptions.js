import React, { useState, useEffect } from "react";
import Cookies from "js-cookie"; // Import js-cookie library
import { useNavigate } from "react-router-dom";

// Components
import LoadingSpinner from "../components/Loader";
import { ColoredTitle, TitleWithSubtitle } from "../components/Titles";
import SubPoints from "../components/SubPoints";

// Assets
import DemoImage from '../assets/images/test.svg';
import LiveImage from '../assets/images/live.svg';
import { Button, Button2 } from "../components/Buttons";
import Gap from "../components/Gap";

const Subscriptions = () => {

    const [loading, setLoading] = useState(false);

    const titleSegments = [
        { text: 'Our ', colorClass: 'text-gray-800' },
        { text: 'Plans ', colorClass: 'text-emerald-500' },
        { text: 'for Your ', colorClass: 'text-gray-800' },
        { text: 'Needs', colorClass: 'text-emerald-500' },
    ];

    return (
        <div className="w-screen h-screen">
            {loading ? (
                <div className="w-full h-full flex justify-center items-center">
                    <LoadingSpinner />
                </div>
            ) : (
                <div className="p-5 bg-white lg:h-full ">
                    <div className="max-w-screen-lg mx-auto mt-20">
                        <ColoredTitle segments={titleSegments} subtitle="In publishing and graphic design, Lorem ipsum is a placeholder text" />
                    </div>
                    <div className="flex flex-col lg:flex-row gap-4 mt-10 lg:mt-20 lg:w-9/12 lg:mx-auto">
                        <div className="bg-gray-100 p-5 rounded-xl lg:flex-1">
                            <TitleWithSubtitle 
                                    title="Basic"
                                    subtitle="In publishing and graphic design, Lorem ipsum is a placeholder text"
                                    color={2} // Change this value to 1 or 2 to test different color schemes
                            />
                            <Gap></Gap>
                            <div className="border-t-2 border-gray-200 py-5">
                            <SubPoints text={'3 types of alerts'} available></SubPoints>
                                <SubPoints text={'Prediction history'} available></SubPoints>
                                <SubPoints text={'No usage statistics'}></SubPoints>
                                <SubPoints text={'Ads'}></SubPoints>
                            </div>
                            <Gap></Gap>
                            <Button2 title="You are already have this" />
                        </div>

                        <div className="bg-cyan-950 p-5 rounded-xl lg:flex-1">
                            <TitleWithSubtitle title="Pro" subtitle="In publishing and graphic design, Lorem ipsum is a placeholder text" span="/ € 20"/>
                            <Gap></Gap>
                            <div className="border-t-2 border-cyan-700 py-5">
                                <SubPoints text={'Everything from basic subscription'} available dark></SubPoints>
                                <SubPoints text={'No Ads'} available dark></SubPoints>
                                <SubPoints text={'Detailed statistical overview'} available dark></SubPoints>
                                <SubPoints text={'Prediction priority '} available dark></SubPoints>
                            </div>
                            <Gap></Gap>
                            <Button title="Upgrade to Pro (coming soon)" />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Subscriptions;
