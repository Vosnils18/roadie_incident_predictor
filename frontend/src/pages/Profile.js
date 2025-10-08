import React, { useState, useEffect } from "react";
import {updateProfile, onAuthStateChanged, sendPasswordResetEmail } from "firebase/auth";
import { getFirestore, doc, setDoc, getDoc } from "firebase/firestore";
import { getStorage, ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { auth } from "../api/firebaseConfig";
import {
    useNavigate,
  } from "react-router-dom";

// Assets
import { ReactComponent as IdIcon } from '../assets/icons/id.svg';
import { ReactComponent as WorldIcon } from '../assets/icons/world.svg';
import { ReactComponent as PremiumIcon } from '../assets/icons/crown.svg';

// Components
import { Button2, Button, Button3, Button4 } from "../components/Buttons";
import { Input, List } from "../components/Inputs";
import { SectionTitle, SectionTitleSmall } from "../components/Titles";
import Gap from "../components/Gap";
import LoadingSpinner from "../components/Loader";

const Profile = () => {
  const storage = getStorage();
  const db = getFirestore();
  const navigate = useNavigate();

  const [displayName, setDisplayName] = useState('');
  const [address, setAddress] = useState('');
  const [profilePic, setProfilePic] = useState('');
  const [profilePicFile, setProfilePicFile] = useState('');
  const [saving, setSaving] = useState(false);
  const [radius, setRadius] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        fetchProfileData();
      }
    });

    return () => {
      unsubscribe();
    };
  }, []);

    const fetchProfileData = async () => {
        try {
        if (auth.currentUser && auth.currentUser.uid) {
            const user = auth.currentUser;
            let photoURL = user.photoURL;
            const userDoc = await getDoc(doc(db, 'users', user.uid));
            if (userDoc.exists()) {
            const userData = userDoc.data();
            console.log('userData:', userData);
            photoURL = photoURL ? photoURL : userData.photoURL || '';
            setDisplayName(userData.displayName || '');
            setAddress(userData.address || '');
            setRadius(userData.radius || '');
            }
            setProfilePic(photoURL);
        } else {
            console.log('No user signed in');
        }
        } catch (error) {
        console.error('Error fetching user data:', error);
        } finally {
        setLoading(false);
        }
    };

    const handleProfilePicChange = (e) => {
        const file = e.target.files[0];
        setProfilePicFile(file);
    };

    const handleUpdateProfile = async () => {
        try {
          const currentUser = auth.currentUser;
          if (currentUser) {
            setSaving(true);
    
            // Check if a new profile picture is selected
            if (profilePicFile) {
              try {
                const storageRef = ref(storage, `users/${currentUser.uid}/profile.jpg`);
                await uploadBytes(storageRef, profilePicFile);
                const photoURL = await getDownloadURL(storageRef);
                await updateProfile(currentUser, { photoURL });
    
                // Update Firestore document with the new photoURL
                await setDoc(doc(db, 'users', currentUser.uid), { photoURL }, { merge: true });
              } catch (uploadError) {
                console.error('Error uploading profile picture:', uploadError);
                alert(`Error uploading profile picture: ${uploadError.message}`);
              }
            }
    
            // Update other profile details
            try {
              await updateProfile(currentUser, { displayName });
            } catch (authError) {
              console.error('Error updating displayName in auth:', authError);
              alert(`Error updating displayName in auth: ${authError.message}`);
            }
    
            // Update Firestore document with other profile details
            try {
              await setDoc(doc(db, 'users', currentUser.uid), {
                displayName,
                address,
                radius
              }, { merge: true });
            } catch (firestoreError) {
              console.error('Error updating Firestore document:', firestoreError);
              alert(`Error updating Firestore document: ${firestoreError.message}`);
            }
    
            setSaving(false);
            window.location.reload();
          } else {
            alert('No user is currently signed in.');
          }
        } catch (error) {
          console.error('Error updating profile:', error);
          alert(`Error updating profile: ${error.message}`);
        }
      };

    const options = [
        { label: "1 km", value: "1" },
        { label: "2 km", value: "2" },
        { label: "5 km", value: "5" },
        { label: "10 km", value: "10" },
    ];

    const handlePasswordReset = async (e) => {
        sendPasswordResetEmail(auth, auth.currentUser.email)
        .then(() => {
            alert('password reset email has been sent!')
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
        });
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
            <div className="mt-20 max-w-screen-md mx-auto">
                <SectionTitle title='Profile Settings' />
                <img
                src={profilePicFile ? URL.createObjectURL(profilePicFile) : (profilePic || 'https://via.placeholder.com/150')}
                alt="Profile"
                className="h-full mx-auto my-10 rounded-lg p-5 max-h-60"
                />
                <div className="flex flex-col gap-2">
                    <Button3 handleProfilePicChange={handleProfilePicChange}></Button3>
                    <Button4 icon={PremiumIcon} title='Go Premium' action={() => {navigate('/subscriptions')}}></Button4>
                </div>
            </div>
            <Gap />
            <div className="flex flex-col max-w-screen-md mx-auto">
                <SectionTitleSmall title={'Display Name'} />
                <Input
                icon={<IdIcon className="h-5 w-5" />}
                placeholder="Display Name"
                value={displayName}
                setValue={setDisplayName}
                />
    
                <Gap />
    
                <SectionTitleSmall title={'Address'} />
                <Input
                icon={<IdIcon className="h-5 w-5" />}
                placeholder="Address"
                value={address}
                setValue={setAddress}
                />
    
                <Gap />
    
                <SectionTitleSmall title={'Radius'} />

                <List
                    icon={<WorldIcon className="h-5 w-5" />}
                    placeholder="Select an option"
                    value={radius}
                    setValue={setRadius}
                    options={options}
                />
    
                <Gap />
    
                <div className="flex flex-col gap-2">
                <Button title={'Change Password'} action={handlePasswordReset}/>
                <Button2 title={'Save Profile'} action={handleUpdateProfile} saving={saving}/>
                </div>
            </div>
            </div>
        )}
        </>
    );
};

export default Profile;