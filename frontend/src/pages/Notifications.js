import React, { useState, useEffect } from "react";
import { getFirestore, collection, query, where, onSnapshot } from "firebase/firestore";
import { getAuth, onAuthStateChanged } from 'firebase/auth';

// Components
import { SectionTitle, SectionTitleSmall } from "../components/Titles";
import Gap from "../components/Gap";
import NotificationWidget from "../components/NotificationWidget";
import LoadingSpinner from "../components/Loader";

const Notifications = () => {
    const [notificationsThisWeek, setNotificationsThisWeek] = useState([]);
    const [olderNotifications, setOlderNotifications] = useState([]);
    const [loading, setLoading] = useState(true); // Add loading state
    const auth = getAuth();
    const db = getFirestore();

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (user) => {
            if (user) {
                fetchNotifications(user.uid);
            }
        });

        return () => {
            unsubscribe();
        };
    }, []);

    const fetchNotifications = (userId) => {
        const userNotificationsQuery = query(
            collection(db, 'notificationHistory'),
            where('user', '==', userId)
        );

        const unsubscribe = onSnapshot(userNotificationsQuery, (snapshot) => {
            const newNotificationsThisWeek = [];
            const newOlderNotifications = [];

            snapshot.forEach((doc) => {
                const notification = doc.data();
                if (isOlderThanSevenDays(notification.timestamp)) {
                    newOlderNotifications.push(notification);
                } else {
                    newNotificationsThisWeek.push(notification);
                }
            });

            // Reverse arrays to show new notifications at the top
            setNotificationsThisWeek(newNotificationsThisWeek.reverse());
            setOlderNotifications(newOlderNotifications.reverse());
            setLoading(false); // Set loading to false once notifications are fetched
        });

        return () => {
            unsubscribe();
        };
    };

    const isOlderThanSevenDays = (timestamp) => {
        // Get the current date
        const currentDate = new Date();
    
        // Convert Firebase Timestamp to JavaScript Date object
        const notificationDate = timestamp.toDate();
    
        // Calculate the difference in milliseconds
        const differenceInMs = currentDate - notificationDate;
    
        // Convert milliseconds to days
        const differenceInDays = differenceInMs / (1000 * 60 * 60 * 24);
    
        // Check if the difference is greater than 7 days
        return differenceInDays > 7;
    };
    

    return (
        <>
            {loading && 
                <div className="w-screen h-screen flex justify-center items-center">
                    <LoadingSpinner />
                </div>
            }
            {!loading && (
                <div className="p-5 bg-white h-full min-h-screen">
                    <div className="mt-20 max-w-screen-lg mx-auto">
                    {notificationsThisWeek.length + olderNotifications.length > 0 ? (
                        <>
                            {notificationsThisWeek.length > 0 && (
                                <>
                                    <SectionTitle title={'Notifications'} />
                                    <Gap />
                                    <SectionTitleSmall title={'This Week'} />
                                    <Gap />
                                    <div className="flex flex-col gap-2">
                                        {notificationsThisWeek.map((notification, index) => (
                                            <NotificationWidget
                                                key={index}
                                                level={notification.title}
                                                body={notification.body}
                                                date={formatDate(notification.timestamp)}
                                            />
                                        ))}
                                    </div>
                                </>
                            )}
                            <Gap />
                            {olderNotifications.length > 0 && (
                                <>
                                    <SectionTitleSmall title={'Older'} />
                                    <Gap />
                                    <div className="flex flex-col gap-2">
                                        {olderNotifications.map((notification, index) => (
                                            <NotificationWidget
                                                key={index}
                                                level={notification.title}
                                                body={notification.body}
                                                date={formatDate(notification.timestamp)}
                                            />
                                        ))}
                                    </div>
                                </>
                            )}
                        </>
                        ) : (
                            <div className="w-full flex justify-center ">
                                <SectionTitleSmall title={"You don't have any notifications"} />
                            </div>
                        )}

                    </div>
                </div>
            )}
        </>
    );
    
}

const formatDate = (timestamp) => {
    const date = timestamp.toDate();
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false // Use 24-hour format
    });
};

export default Notifications;