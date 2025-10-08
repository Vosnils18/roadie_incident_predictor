importScripts("https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging-compat.js");

 //the Firebase config object 
const firebaseConfig = {
    // apiKey: ,
    // authDomain: ,
    // projectId: ,
    // storageBucket: ,
    // messagingSenderId: ,
    // appId: 
  };

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();


messaging.onBackgroundMessage(function(payload) {
  console.log('Received background message ', payload);
  const notificationTitle = payload.notification.title;
  const notificationBody = payload.notification.body;

  if ('serviceWorker' in navigator && 'Notification' in window) {
    const options = {
      body: notificationBody,
    };
    navigator.serviceWorker.ready.then(function(registration) {
      registration.showNotification(notificationTitle, options);
    });
  }
});