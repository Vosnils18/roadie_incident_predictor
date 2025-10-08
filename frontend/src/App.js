import React, { useState, useEffect, useLayoutEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
  useNavigate,
} from "react-router-dom";
import Cookies from "js-cookie";
import { onAuthStateChanged } from "firebase/auth";
import { doc, getDoc, setDoc, getFirestore } from 'firebase/firestore';
import { auth } from "./api/firebaseConfig"; // Adjust the import path as necessary


import './App.css';
import './assets/styles/transitions.css';

// Pages
import Auth from '../src/pages/Auth';
import Dashboard from '../src/pages/Dashboard';
import Notifications from "./pages/Notifications";
import Profile from "./pages/Profile";
import Statistics from "./pages/Statistics";
import Mode from "./pages/Mode";
import Subscriptions from "./pages/Subscriptions";
import Tutorial from "./pages/Tutorial";

// Components
import Navbar from "./components/Navbar";
import Menu from "./components/Menu";
import LoadingSpinner from "./components/Loader"; // Import your loading spinner component


//API
import NotificationListener from "./api/notification";
import DeviceListener from "./api/specs";

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

function AppContent() {
  const location = useLocation();
  const navigate = useNavigate();
  const db = getFirestore();
  const cookieMode = Cookies.get('mode');
  const shouldShowNavbar = !['/auth', '/mode', '/tutorial'].includes(location.pathname);

  const [isMenuOpen, setIsMenuOpen] = useState(false); // State to track menu open/close
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true); // State to track loading status

  const handleMenu = () => {
    // Toggle the state of the menu
    setIsMenuOpen(!isMenuOpen);
  };

  useEffect(() => {
    // Close the menu when the location changes
    setIsMenuOpen(false);
  }, [location]);

  useEffect(() => {
    // Check the user's authentication state
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      setUser(user);
      setLoading(false); // Set loading to false after checking authentication state

      if (user) {
        // Fetch the user data from Firestore
        try {
          const userDoc = await getDoc(doc(db, 'users', user.uid));
          
          if (userDoc.exists()) {
            const userData = userDoc.data();
            console.log('User data fetched:', userData);

            // Check if it's the user's first login
            if (userData.firstLogin === true) {
              console.log('First login detected, navigating to /tutorial');
              navigate('/tutorial');
            } else {
              console.log('Not first login');
              if (!cookieMode || (cookieMode !== 'demo' && cookieMode !== 'live')) {
                console.log('Invalid cookie mode, navigating to /mode');
                navigate('/mode');
              } 

              else {
                console.log('Valid cookie mode:', cookieMode);
              }
            }
          } else {
            await setDoc(doc(db, 'users', user.uid), {
              displayName: user.displayName,
              firstLogin: true // Set firstLogin to true for initial login
              // Add more initial fields as needed
            });
            navigate('/tutorial');
          }
        } catch (error) {
          console.error('Error fetching user document:', error);
        }
      }
    });

    // Cleanup subscription on unmount
    return () => unsubscribe();
  }, [cookieMode, navigate]);

  

  if (loading) {
    // Show loading spinner while checking authentication state
    return (
      <div className="flex h-screen justify-center items-center">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="relative"> 
      {cookieMode == "live" && <DeviceListener></DeviceListener>}
      <NotificationListener></NotificationListener>
      {shouldShowNavbar && <Navbar color={'cyan-900'} action={handleMenu} />}
      {shouldShowNavbar && <Menu action={handleMenu} isMenuOpen={isMenuOpen} />}
      <div className="content"> {/* Optional: Add a wrapper for the content */}
        <Routes>
          <Route path='/' element={<Dashboard />} />
          <Route path='/auth' element={<Auth />} />
          <Route path='/profile' element={<Profile />} />
          <Route path='/mode' element={<Mode />} />
          <Route path='/tutorial' element={<Tutorial />} />
          <Route path='/statistics' element={<Statistics />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/subscriptions" element={<Subscriptions />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
