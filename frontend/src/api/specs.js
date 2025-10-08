import React, { useEffect, useState } from 'react';

const GyroscopeComponent = () => {
  const [gyroscopePermission, setGyroscopePermission] = useState(null);

  useEffect(() => {
    const handlePermission = () => {
      if (typeof DeviceOrientationEvent.requestPermission === 'function') {
        DeviceOrientationEvent.requestPermission()
          .then(permissionState => {
            if (permissionState === 'granted') {
              setGyroscopePermission(true);
            } else {
              setGyroscopePermission(false);
            }
          })
          .catch(console.error);
      } else {
        setGyroscopePermission(true); // Permission not required for iOS Safari
      }
    };

    handlePermission();
  }, []);

};

export default GyroscopeComponent;
