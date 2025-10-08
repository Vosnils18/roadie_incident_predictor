import React, { useState, useEffect } from 'react';
import { CSSTransition, SwitchTransition } from 'react-transition-group';
import { useNavigate } from "react-router-dom";
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, getAuth, updateProfile, onAuthStateChanged, GoogleAuthProvider, signInWithRedirect, sendPasswordResetEmail  } from 'firebase/auth';
import { auth } from '../api/firebaseConfig';

//Assets
import loginImage from '../assets/images/login.svg';
import registerImage from '../assets/images/undraw_undraw_undraw_undraw_sign_up_ln1s_-1-_s4bc_-1-_ee41_-1-_kf4d.svg'
import { ReactComponent as EmailIcon }  from '../assets/icons/email.svg'
import { ReactComponent as IdIcon }  from '../assets/icons/id.svg'
import { ReactComponent as PasswordIcon }  from '../assets/icons/lock.svg'

//Components
import {TitleWithSubtitle} from '../components/Titles';
import { Input, PasswordInput } from '../components/Inputs'; // Assuming the file is named InputComponents.js
import {Button, GoogleButton, TextButton} from '../components/Buttons';
import Gap from '../components/Gap'
import Checkbox from '../components/Checkbox'
import LoadingSpinner from '../components/Loader'

const Auth = () => {

    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(0)
    const navigate = useNavigate();
    const auth = getAuth();

    useEffect(() => {
      // Listen for authentication state changes
      const unsubscribe = onAuthStateChanged(auth, user => {
        if (user) {
        } else {
          // If no user is logged in, set loading to false
          setLoading(false);
        }
      });
  
      // Clean up subscription when component unmounts
      return () => unsubscribe();
    }, [auth, navigate]);

    const [popupWindow, setPopupWindow] = useState(null);
    const [error, setError] = useState(null);

    const handleGoogleLogin = async () => {
        const provider = new GoogleAuthProvider();
        try {
            const result = await signInWithRedirect(auth, provider);
            const user = result.user;
            // Handle successful Google login, if needed
            alert('Google login successful');
        } catch (err) {
            setError(err.message);
        }
    };

    const SignIn = () => {
      const [email, setEmail] = useState('');
      const [password, setPassword] = useState('');
      const navigate = useNavigate();
      const auth = getAuth();

  
      useEffect(() => {
          // Listen for authentication state changes
          const unsubscribe = onAuthStateChanged(auth, user => {
              if (user) {
                  // If user is logged in, redirect to '/'
                  navigate('/');
              }
          });
  
          // Clean up subscription when component unmounts
          return () => unsubscribe();
      }, [auth, navigate]);
  
      const handleLogin = async (e) => {
          e.preventDefault();
          try {
              // Ensure both email and password are provided before attempting login
              if (!email || !password) {
                  setError('Please provide both email and password.');
                  return;
              }
              await signInWithEmailAndPassword(auth, email, password);
              alert('Login successful');
          } catch (err) {
              setError(err.message);
          }
      };

      const handlePasswordReset = async (e) => {
        if (email)
          {
            sendPasswordResetEmail(auth, email)
            .then(() => {
                alert('password reset email has been sent!')
                setError('')
            })
            .catch((error) => {
                const errorCode = error.code;
                const errorMessage = error.message;
            });
          }
          else
          {
            setError('Type your email!')
          }
      };
  
  
      return (
          <div className="flex md:flex-row flex-col md:justify-around w-full md:max-w-4xl">
              <img src={loginImage} alt="Login" className="mb-8 md:max-w-80 lg:mt-0 mt-10" />
              <div className="flex flex-col">
                  <TitleWithSubtitle title="Login" subtitle="Use your email and password to login" />
                  <Gap />
                  <Input
                      icon={<EmailIcon className="h-5 w-5" />}
                      placeholder="Email"
                      value={email}
                      setValue={setEmail}
                  />
                  <PasswordInput
                      icon={<PasswordIcon className="h-5 w-5 fill-cyan-900" />}
                      placeholder="Password"
                      value={password}
                      setValue={setPassword}
                  />
                  {error && <p className="text-red-500 text-center">{error}</p>}
                  <TextButton title="Forgot your password?" position="right" color="cyan-900" decoration="underline" action={handlePasswordReset}/>
                  <Gap />
                  <Button title="Login" color="red-200" action={handleLogin} />
                  <p className="text-center my-4 text-cyan-900">OR</p>
                  <GoogleButton title="Continue with Google" action={handleGoogleLogin} />
                  <p onClick={() => setPage(1)} className="text-center my-2 text-cyan-900 cursor-pointer">
                      Don't have an account yet? <span className="text-cyan-600">Sign up!</span>
                  </p>
              </div>
          </div>
      );
    };

    const SignUp = () => {
      const [isChecked, setIsChecked] = useState(false);
      const [email, setEmail] = useState('');
      const [displayName, setDisplayName] = useState('');
      const [password, setPassword] = useState('');
      const [passwordAgain, setPasswordAgain] = useState('');
      const [error, setError] = useState(null);
  
      const handleChange = (event) => {
          setIsChecked(event.target.checked);
      };
  
      const handleRegister = async (e) => {
        e.preventDefault();
        try {
          // Ensure all required fields are provided
          if (!email || !password || !passwordAgain || !displayName) {
            setError('Please provide all required fields.');
            return;
          }
    
          // Check if passwords match
          if (passwordAgain !== password) {
            setError('Passwords do not match.');
            return;
          }
    
          // Check if checkbox is checked
          if (!isChecked) {
            setError('You must agree to the terms and conditions.');
            return;
          }
    
          // Create user with email and password
          const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    
          // Update profile with display name
          await updateProfile(userCredential.user, {
            displayName: displayName,
          });
    
          alert('Registration successful!');
          navigate('/')
        } catch (err) {
          setError(err.message);
        }
      };
  
      return (
          <div className='flex md:flex-row flex-col md:justify-around w-full md:max-w-4xl'>
              <img src={registerImage} alt="Login" className='mb-8 md:max-w-80 lg:mt-0 mt-10' />
              <div className='flex flex-col'>
                  <TitleWithSubtitle title='Register' subtitle='Use your email and password to login' />
                  <Gap />
                  <Input
                      icon={<IdIcon className="h-5 w-5" />}
                      placeholder="Full Name"
                      value={displayName}
                      setValue={setDisplayName}
                  />
                  <Input
                      icon={<EmailIcon className="h-5 w-5" />}
                      placeholder="Email"
                      value={email}
                      setValue={setEmail}
                  />
                  <PasswordInput
                      icon={<PasswordIcon className="h-5 w-5 fill-cyan-900" />}
                      placeholder="Password"
                      value={password}
                      setValue={setPassword}
                  />
                  <PasswordInput
                      icon={<PasswordIcon className="h-5 w-5 fill-cyan-900" />}
                      placeholder="Password"
                      value={passwordAgain}
                      setValue={setPasswordAgain}
                  />
                  <div className="flex items-center">
                      <Checkbox label="I agree with all Terms And Conditions" onChange={handleChange} checked={isChecked} />
                  </div>
                  {error && <p className="text-red-500 text-center">{error}</p>}
                  <Gap />
                  <Button title='Register' action={handleRegister} />
                  <p className='text-center my-4 text-cyan-900'>OR</p>
                  <GoogleButton title="Continue with Google" action={handleGoogleLogin} />
                  <p onClick={() => { setPage(0) }} className='text-center my-2 text-cyan-900'>Already have an account? <span className='text-center my-2 text-cyan-600'>Sign in!</span></p>
              </div>
          </div>
      )
  }
  
    return (
      <div className="bg-cyan-950 p-5 m-5 flex justify-center items-center h-screen">
        {/* Show loading screen while loading is true */}
        {loading ? (
          <div>
            <LoadingSpinner></LoadingSpinner>
          </div>
        ) : (
          <SwitchTransition>
            <CSSTransition
              key={page}
              addEndListener={(node, done) => {
                node.addEventListener('transitionend', done, false);
              }}
              classNames="fade"
            >
              {page === 0 ? <SignIn /> : <SignUp />}
            </CSSTransition>
          </SwitchTransition>
        )}
      </div>
    );
  };

export default Auth;