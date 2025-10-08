import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { onAuthStateChanged } from "firebase/auth"; // Import the onAuthStateChanged function
import { auth } from "../api/firebaseConfig"; // Import the auth instance
import Cookies from "js-cookie";

// Components
import { TitleWithSubtitle, SectionTitle, SectionTitleSmall } from "../components/Titles";
import LoadingSpinner from "../components/Loader";
import Predictions from "../components/Prediction";
import MapWithHeatmap from "../components/Map";
import Gap from "../components/Gap";
import Details from "../components/Details";
import { CSSTransition, SwitchTransition } from "react-transition-group";

// Api
import { fetchDataEveryTwoMinutes } from "../api/call";

const Dashboard = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState(undefined); // Initialize user state with undefined
    const [details, setDetails] = useState(false);
    const cookieMode = Cookies.get('mode');
    const [prediction, setPrediction] = useState(null);

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
            if (currentUser) {
                setUser(currentUser);
                if (cookieMode === 'demo' || cookieMode === 'live') {
                    const fetchDataEveryTwoMinutesWithInterval = async (mode) => {
                        try {
                            const data = await fetchDataEveryTwoMinutes(mode);
                            setPrediction(data);  // Update prediction state with fetched data
                        } catch (error) {
                            console.error('Error fetching data every two minutes:', error);
                        }
                    };

                    // Immediately invoke fetchDataEveryTwoMinutesWithInterval once with mode
                    fetchDataEveryTwoMinutesWithInterval(cookieMode);

                    // Set interval to run fetchDataEveryTwoMinutesWithInterval every 2 minutes with mode
                    const interval = setInterval(() => fetchDataEveryTwoMinutesWithInterval(cookieMode), 2 * 60 * 1000);

                    // Clean up interval on component unmount
                    return () => clearInterval(interval);
                }
            } else {
                navigate('/auth'); // Redirect to login if no user is logged in
            }
        });

        // Cleanup the subscription
        return () => unsubscribe();
    }, [cookieMode]);  // Depend on cookieMode to trigger updates
    // Render loading spinner if user state is undefined
    if (user === undefined) {
        return (
            <div className="flex h-screen justify-center items-center">
                <LoadingSpinner />
            </div>
        );
    }
    


    return (
        <div className="h-screen ">
            <div className="p-5 mt-16 mb-10 z-0 max-w-screen-xl mx-auto" id="title-with-subtitle">
                <TitleWithSubtitle title={`Welcome, \n ${user.displayName ? user.displayName.split(' ')[0] : user.email.split('@')[0]}!`} subtitle="version: v0.9.3 - beta" />
            </div>

            <div className="w-full bg-white h-fill rounded-t-3xl p-5 z-10">
                <div className="max-w-screen-xl mx-auto">
                    <div className="flex gap-2 justify-center">
                        <div className={`w-24  mb-4 h-1 bg-gray-200  rounded-xl`}></div>
                    </div>
                    <SwitchTransition>
                        <CSSTransition
                            key={details}
                            addEndListener={(node, done) => {
                                node.addEventListener('transitionend', done, false);
                            }}
                            classNames="slide"
                            >
                            

                            {
                                details === true ? (
                                    <Details setDetails={setDetails} />
                                ) : (
                                    <div>
                                    <SectionTitle title={'Predictions'} />
                                    <div className="snap-x flex overflow-x-auto gap-4 my-5">
                                        {prediction == null ? (
                                        <LoadingSpinner />
                                        ) : prediction.prediction ? (
                                        <Predictions type='low' prediction={prediction.prediction}  action={() => {}}/>
                                        ) : (
                                        <Predictions type='placeholder' />
                                        )}
                                    </div>
                                    <SectionTitleSmall title={'Live map'} />
                                    <Gap />
                                    {prediction == null ? (
                                        <div className="h-dvh">
                                            <LoadingSpinner />
                                        </div>
                                        ) : prediction.prediction ? (
                                        <MapWithHeatmap />
                                        ) : (
                                        <Predictions type='placeholder' />
                                        )}
                                    </div>
                                )
                            }

                            
                        </CSSTransition>
                    </SwitchTransition>
                </div>

            </div>
        </div>
    );
}

export default Dashboard;
