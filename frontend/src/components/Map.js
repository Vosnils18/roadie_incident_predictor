import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Rectangle, Circle, ZoomControl } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.heat/dist/leaflet-heat.js';
import LoadingSpinner from './Loader';
import Cookies from 'js-cookie'; // Import js-cookie library

const MapWithHeatmap = ({ data }) => {
  const [center, setCenter] = useState(null); // Initialize center as null
  const mapRef = useRef(null);

  useEffect(() => {
    const cookieMode = Cookies.get('mode');
    if (cookieMode === 'demo') {
      setCenter([51.571915, 4.768323]); // Set center to demo location
    } else {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords;
            setCenter([latitude, longitude]);
          },
          (error) => {
            console.error('Error obtaining location:', error);
            // Optionally, set a default center if there's an error
            setCenter([51.505, -0.09]);
          }
        );
      } else {
        console.log('Geolocation is not supported by this browser.');
        // Optionally, set a default center if geolocation is not supported
        setCenter([51.505, -0.09]);
      }
    }
  }, []);

  const redOptions = { color: 'red' };
  const greeOptions = { color: 'green' };
  const orangeOptions = { color: 'orange' };
  const blueOptions = { color: 'lightblue'};

  const rectangle = center ? [
    [center[0], center[1]],
    [center[0] - 0.0001, center[1] - 0.0001],
  ] : null;

  // Conditionally render the MapContainer only if center is set
  return (
    center ? (
      <MapContainer
        center={center}
        zoom={18}
        ref={mapRef}
        scrollWheelZoom={true}
        style={{ height: '70vh', width: '100%' }}
        className="rounded-lg"
        zoomControl={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={center}>
        </Marker>
        <Circle center={center} pathOptions={blueOptions} radius={1000} />
        
        <Rectangle bounds={rectangle} pathOptions={greeOptions} />
      </MapContainer>
    ) : (
      <div className='h-screen'><LoadingSpinner /></div> // Optional loading indicator while waiting for center
    )
  );
};

export default MapWithHeatmap;
