// src/firebaseConfig.js
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getMessaging } from "firebase/messaging";


const firebaseConfig = {
    // apiKey: ,
    // authDomain: ,
    // projectId: ,
    // storageBucket: ,
    // messagingSenderId: ,
    // appId: 
  };
  
// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const messaging = getMessaging(app);
