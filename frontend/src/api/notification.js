import React, { useState, useEffect } from 'react';
import { messaging } from '../api/firebaseConfig';
import { getToken, onMessage } from 'firebase/messaging';
import { getFirestore, doc, setDoc, Timestamp } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

function Notification() {
  const [notification, setNotification] = useState({ title: '', body: '' });
  const db = getFirestore();
  const auth = getAuth();

  useEffect(() => {
    const requestPermission = async () => {
      console.log("Requesting User Permission...");

      try {
        const permission = await window.Notification.requestPermission();
        if (permission === "granted") {
          console.log("Notification User Permission Granted.");
          const currentToken = await getToken(messaging, { vapidKey: 'BCIQpqvNeJqERdY72az6TVwv3jvtvWZAizYYZ5eP023fXSV_KaD0NucwMx6d53cPOA0b1qufPO8NzP5BLz7gdGY' });
          if (currentToken) {
            console.log('Client Token: ', currentToken);
          } else {
            console.log('Failed to generate the app registration token.');
          }
        } else {
          console.log("User Permission Denied.");
        }
      } catch (error) {
        console.error('An error occurred when requesting permission:', error);
      }
    };

    const onMessageListener = () =>
      new Promise((resolve) => {
        onMessage(messaging, (payload) => {
          resolve(payload);
        });
      });

    const saveNotificationToHistory = async (notification) => {
      console.log('saveNotificationToHistory called with:', notification);
      const user = auth.currentUser;
      if (user) {
        try {
          const notificationDoc = {
            title: notification.title,
            body: notification.body,
            timestamp: Timestamp.now(),
            user: user.uid,
          };
          const docRef = doc(db, 'notificationHistory', `${user.uid}_${Date.now()}`);
          await setDoc(docRef, notificationDoc);
          console.log('Notification saved to history:', notificationDoc);
        } catch (error) {
          console.error('Error saving notification to history:', error);
        }
      } else {
        console.log('No user is signed in, cannot save notification.');
      }
    };

    requestPermission();

    const unsubscribe = onMessageListener()
      .then((payload) => {
        const receivedNotification = {
          title: payload?.notification?.title,
          body: payload?.notification?.body,
        };
        console.log('Notification payload received:', payload);
        setNotification(receivedNotification);
        saveNotificationToHistory(receivedNotification);
        console.log('Notification processed:', receivedNotification);
      })
      .catch((err) => {
        console.error('Failed to subscribe to messages:', err);
      });

    return () => {
      unsubscribe.then(() => {
        console.log('Unsubscribed from messages');
      }).catch((err) => {
        console.log('Failed to unsubscribe from messages:', err);
      });
    };
  }, [auth, db]);

  return null; // Since we're not using toast, returning null to render nothing
}

export default Notification;
