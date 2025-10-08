import React, { useState } from "react";
import { TitleWithSubtitle } from "../components/Titles";
import { getFirestore, doc, setDoc, Timestamp } from 'firebase/firestore';
import { SwitchTransition, CSSTransition } from "react-transition-group";
import { getAuth } from 'firebase/auth';

//Components
import Gap from "../components/Gap";
import { ReactComponent as ArrowIcon } from '../assets/icons/angle.svg';
import { Navigate, useNavigate } from "react-router-dom";
import { Button } from "../components/Buttons";

//Assets
import Tutorial1Image from '../assets/images/tutorial_1.svg';
import Tutorial2Image from '../assets/images/tutorial_2.svg';
import Tutorial3Image from '../assets/images/tutorial_3.svg';
import Tutorial4Image from '../assets/images/tutorial_4.svg';

const Tutorial = () => {
    const [page, setPage] = useState(0);
    const db = getFirestore();
    const auth = getAuth();
    const navigate = useNavigate();  // Invoke useNavigate

    const handlePage = () => {
        setPage(page + 1);
    }

    const handleStart = async () => {
        await updateProfile();  // Call updateProfile function
        navigate('/mode');  // Use navigate function
    }

    const updateProfile = async () => {
        const user = auth.currentUser;
        if(user) {
            await setDoc(doc(db, "users", user.uid), {
                firstLogin: false,
            }, { merge: true });
        }
    }

    return (
        <div className="h-screen relative overflow-x-hidden">
            <div className="p-5 flex justify-end">
                <h1 className="text-cyan-600" onClick={handleStart}>skip</h1>
            </div>
            <div className="mt-16 mx-auto w-fit">
                <SwitchTransition>
                    <CSSTransition
                        key={page}
                        addEndListener={(node, done) => {
                            node.addEventListener('transitionend', done, false);
                        }}
                        classNames="fade"
                    >
                        {
                            page === 0 ? (
                                <img src={Tutorial1Image} alt="Tutorial" className="h-96 w-96" />
                            ) :
                            page === 1 ? (
                                <img src={Tutorial2Image} alt="Tutorial" className="h-96 w-96" />
                            ) :
                            page === 2 ? (
                                <img src={Tutorial3Image} alt="Tutorial" className="h-96 w-96" />
                            ) :
                            page === 3 ? (
                                <img src={Tutorial4Image} alt="Tutorial" className="h-96 w-96" />
                            ) :
                            null
                        }
                    </CSSTransition>
                </SwitchTransition>
            </div>
            <div className="absolute md:relative md:w-6/12 md:mx-auto bottom-10 left-0 p-5">
                <SwitchTransition>
                    <CSSTransition
                        key={page}
                        addEndListener={(node, done) => {
                            node.addEventListener('transitionend', done, false);
                        }}
                        classNames="slide"
                    >
                        {
                            page === 0 ? (
                                <>
                                    <div className="mt-10">
                                        <div className="flex gap-2 justify-center">
                                            <div className="h-1 w-full rounded-md bg-emerald-400"></div>
                                            <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                            <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                            <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                        </div>
                                        <Gap />
                                        <TitleWithSubtitle title="Driving comes with many dangers." subtitle="Take care of yourself and stay informed about your routes with reliable predictions and alerts for a safe and efficient journey." />
                                    </div>
                                    <Gap />
                                    <Button title="Get Started" action={handlePage}></Button>
                                </>
                            ) :
                            page === 1 ? (
                                <>
                                    <div className="mt-10">
                                        <div className="flex gap-2 justify-center">
                                            <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                            <div className="h-1 w-full rounded-md bg-emerald-400"></div>
                                            <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                            <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                        </div>
                                        <Gap />
                                        <TitleWithSubtitle title="Get a real-time AI traffic predictions." subtitle="Navigate every drive with confidence. Roadie provides real-time traffic predictions and safety alerts to help you reach your destination safely and efficiently." />
                                    </div>
                                    <Gap />
                                    <Button title="Next" action={handlePage}></Button>
                                </>
                            ) :
                            page === 2 ? (
                                <>
                                    <div className="mt-10">
                                        <div className="flex gap-2 justify-center">
                                            <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                            <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                            <div className="h-1 w-full rounded-md bg-emerald-400"></div>
                                            <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                        </div>
                                        <Gap />
                                        <TitleWithSubtitle title="Customizing alerts for optimized driving." subtitle="Adjust the sensitivity of traffic predictions and set thresholds for alerts. Tailor these settings to receive notifications only when necessary, ensuring you stay informed without the clutter." />
                                    </div>
                                    <Gap />
                                    <Button title="Next" action={handlePage}></Button>
                                </>
                            ) :
                            page === 3 ? (
                                <>
                                    <div className="flex gap-2 justify-center mt-10">
                                        <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                        <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                        <div className="h-1 w-full rounded-md bg-cyan-800"></div>
                                        <div className="h-1 w-full rounded-md bg-emerald-400"></div>
                                    </div>
                                    <Gap />
                                    <TitleWithSubtitle title="Access and analyze driving statistics." subtitle="Keep track of your driving patterns and alert history with detailed statistics. Analyze past routes, times, and the frequency of alerts to understand your driving habits better and identify potential areas for improvement." />
                                    <Gap />
                                    <Button title="Finish" action={handleStart}></Button> {/* Updated to call handleStart */}
                                </>
                            ) :
                            null
                        }
                    </CSSTransition>
                </SwitchTransition>
            </div>
        </div>
    );
}

export default Tutorial;
