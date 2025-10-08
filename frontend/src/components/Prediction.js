import React from "react";

//Components
import { ReactComponent as LocationIcon }  from '../assets/icons/location-exclamation.svg'


const Predictions = ({ type, action, prediction }) => {

    const handleDetails = () => {
        action();
    }

    const Low = () => (
        <div className="snap-center bg-emerald-400 p-5 rounded-xl border-l-2 border-r-2 border-t-2 border-b-4 border-emerald-500 cursor-pointer" onClick={handleDetails}> 
          <div>
            <div className="flex gap-4 items-center">
              <div className="bg-white rounded-md p-2">
                <LocationIcon className='h-8 w-8 fill-emerald-400'></LocationIcon>
              </div>
              <div>
                <h1 className="text-emerald-600 font-bold text-2xl">{((prediction)).toFixed(2)} %</h1>
                <h3 className="text-white font-semibold">Graaf Engelbertlaan</h3>
              </div>
            </div>
            <h2 className="text-white mt-3 w-64">Accident probability in the area is low. Drive safely and enjoy your journey.</h2>
          </div>
        </div>
      );

    const Medium = () => (
        <div className="snap-center  bg-orange-200 p-5 rounded-xl border-l-2 border-r-2 border-t-2 border-b-4 border-orange-300 cursor-pointer" onClick={handleDetails}> 
            <div>
                <div className="flex gap-4 items-center">
                    <div className="bg-white rounded-md p-2">
                        <LocationIcon className='h-8 w-8 fill-orange-300'></LocationIcon>
                    </div>
                    <div>
                        <h1 className="text-orange-500 font-bold text-2xl">Low</h1>
                        <h3 className="text-white font-semibold">Johan Willem Frisolaan 27-15, 4835 AA Breda</h3>
                    </div>
                </div>
                <h2 className="text-white mt-3 w-64">Caution: The likelihood of an accident is significantly increased, with speeding presenting the highest risk. Consider slowing down or seeking an alternate route to minimize the risk of accidents.</h2>
            </div>
        </div>
    );

    const High = () => (
        <div className="snap-center  bg-red-300 p-5 rounded-xl border-l-2 border-r-2 border-t-2 border-b-4 border-red-400 cursor-pointer" onClick={handleDetails}> 
            <div>
                <div className="flex gap-4 items-center">
                    <div className="bg-white rounded-md p-2">
                        <LocationIcon className='h-8 w-8 fill-red-400'></LocationIcon>
                    </div>
                    <div>
                        <h1 className="text-red-500 font-bold text-2xl">Low</h1>
                        <h3 className="text-white font-semibold">Johan Willem Frisolaan 27-15, 4835 AA Breda</h3>
                    </div>
                </div>
                <h2 className="text-white mt-3 w-64">Caution: The likelihood of an accident is significantly increased, with speeding presenting the highest risk. Consider slowing down or seeking an alternate route to minimize the risk of accidents.</h2>
            </div>
        </div>
    );

    const Placeholder = () => (
        <div className="snap-center  bg-gray-50 p-5 rounded-xl border-l-2 border-r-2 border-t-2 border-b-4 border-gray-100" > 
            <div>
                <div className="flex gap-4 items-center justify-center">
                    <div>
                        <h1 className="text-gray-500 font-bold text-2xl text-center">No more</h1>
                        <h3 className="text-gray-200 font-semibold text-center">No more prediction on the area</h3>
                    </div>
                </div>
            
            </div>
        </div>
    );

    return (
        <>
            {type === 'low' && <Low />}
            {type === 'medium' && <Medium />}
            {type === 'high' && <High />}
            {type === 'placeholder' && <Placeholder />}
        </>
    );
}

export default Predictions;
