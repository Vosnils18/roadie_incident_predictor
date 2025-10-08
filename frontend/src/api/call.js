// api.js

import axios from 'axios';

const API_KEY = 'bedbb10b6a5a69c319ba8e8ae7288122'; // Replace with your actual API key
const API_BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall';

// Function to fetch location using browser's geolocation API
const fetchLocation = () => {
  return new Promise((resolve, reject) => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
        },
        (error) => {
          reject(error);
        }
      );
    } else {
      reject(new Error('Geolocation is not supported.'));
    }
  });
};

// Function to fetch real-time weather data from OpenWeatherMap
const fetchWeatherData = async (latitude, longitude) => {
  try {
    const response = await axios.get(API_BASE_URL, {
      params: {
        lat: latitude,
        lon: longitude,
        appid: API_KEY,
        units: 'metric', // or 'imperial' for Fahrenheit
      },
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch weather data.');
  }
};

// Function to get current time
const getCurrentTime = () => {
  const now = new Date();
  return {
    currentTime: now.toLocaleTimeString(),
  };
};

// Exporting API functions
export const fetchInitialData = async () => {
  try {
    const location = await fetchLocation();
    const weatherData = await fetchWeatherData(location.latitude, location.longitude);
    const currentTime = getCurrentTime();
    return { location, weatherData, currentTime };
  } catch (error) {
    console.error('Error fetching initial data:', error);
    throw error;
  }
};


export const fetchDataEveryTwoMinutes = async (mode) => {
  try {
      if (mode === 'live') {
          const data = await fetchInitialData();
          console.log('Data fetched at:', new Date().toLocaleTimeString());
          console.log(data);
          // Example of a live API call using axios
          // const response = await axios.post('https://backend.example.com/predict', data);
          // console.log('Backend API response:', response.data);
      } else if (mode === 'demo') {
          const data = {
              "temp": 11.5,
              "rain": 0,
              "streetname": "Manhuisveld",
              "gforce": 2.8,
              "speedlimit": 10,
              "windspeed": 2.0,
              "datetime": new Date().toISOString()  // Ensure datetime is in ISO format
          };

          console.log('Demo data fetched at:', new Date().toLocaleTimeString());
          console.log(data);

          const response = await axios.post('https://model.balage.top/api/predictions/make_predictions/', data, {
              headers: {
                  'Content-Type': 'application/json',
              },
          });

          return(response.data)
      } else {
          console.error('Invalid mode');
      }
  } catch (error) {
      console.error('Error fetching data every two minutes:', error);
  }
};