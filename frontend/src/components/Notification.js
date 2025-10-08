import React, { useState, useEffect } from 'react';

function Notification() {
  const [notification, setNotification] = useState({ title: '', body: '' });

  useEffect(() => {
    const requestPermission = async () => {
      console.log("Requesting User Permission...");

      try {
        const permission = await window.Notification.requestPermission();
        if (permission === "granted") {
          console.log("Notification User Permission Granted.");
        } else {
          console.log("User Permission Denied.");
        }
      } catch (error) {
        console.error('An error occurred when requesting permission:', error);
      }
    };

    const onMessageListener = () =>
      new Promise((resolve) => {
        // Simulating onMessage handler
        setTimeout(() => {
          resolve({ notification: { title: 'Sample Title', body: 'Sample Body' } });
        }, 2000); // Simulated delay of 2 seconds
      });

    const saveNotificationToHistory = async (notification) => {
      // Simulating saving notification to history
      console.log('Notification saved to history:', notification);
    };

    requestPermission();

    const unsubscribe = onMessageListener().then((payload) => {
      const receivedNotification = {
        title: payload?.notification?.title,
        body: payload?.notification?.body,
      };
      setNotification(receivedNotification);
      saveNotificationToHistory(receivedNotification);
      console.log('Notification received:', receivedNotification);
    
    }).catch((err) => {
      console.error('Failed to subscribe to messages:', err);
    });

    return () => {
      unsubscribe.catch((err) => console.log('Failed to unsubscribe from messages:', err));
    };
  }, []);

  return null; // Since we're not using toast, returning null to render nothing
}

export default Notification;
