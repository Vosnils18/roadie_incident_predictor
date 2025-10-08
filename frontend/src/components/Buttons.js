import React, {useState, useRef} from "react";

//Components
import LoadingSpinner from "./Loader";

//Assets
import Google from '../assets/icons/google.png'

export const Button = ({ title, action, saving }) => {
    const [isPressed, setIsPressed] = useState(false);
  
    const handlePressStart = () => {
      setIsPressed(true);
    };
  
    const handlePressEnd = () => {
      setIsPressed(false);
    };
  
    return (
      <div
        className={`cursor-pointer flex justify-center p-3 rounded-md h-14 items-center ${
          isPressed
            ? 'bg-emerald-400 border-emerald-600 border-b-2 border-r-2 border-l-2 border-t-2'
            : 'bg-emerald-400 border-emerald-600 border-b-4 border-r-2 border-l-2 border-t-2'
        }`}
        onClick={action}
        onMouseDown={handlePressStart}
        onMouseUp={handlePressEnd}
        onMouseLeave={handlePressEnd}
        onTouchStart={handlePressStart}
        onTouchEnd={handlePressEnd}
      >
        <h1 className="text-white font-bold">{saving ? <LoadingSpinner/> : title }</h1>
      </div>
    );
  };

export const Button2 = ({ title, action, saving }) => {
    const [isPressed, setIsPressed] = useState(false);
  
    const handlePressStart = () => {
      setIsPressed(true);
    };
  
    const handlePressEnd = () => {
      setIsPressed(false);
    };
  
    return (
      <div
        className={`cursor-pointer flex justify-center p-3 rounded-md h-14 items-center ${
          isPressed
            ? 'bg-cyan-800 border-cyan-900 border-b-2 border-r-2 border-l-2 border-t-2'
            : 'bg-cyan-800 border-cyan-900 border-b-4 border-r-2 border-l-2 border-t-2'
        }`}
        onClick={action}
        onMouseDown={handlePressStart}
        onMouseUp={handlePressEnd}
        onMouseLeave={handlePressEnd}
        onTouchStart={handlePressStart}
        onTouchEnd={handlePressEnd}
      >
        <h1 className="text-white font-bold">{saving ? <LoadingSpinner/> : title }</h1>
      </div>
    );
  };

export const Button3 = ({ handleProfilePicChange }) => {
    const fileInputRef = useRef(null);

    const handleClick = () => {
      fileInputRef.current.click();
    };
  
    return (
      <div className="cursor-pointer flex justify-center p-3 rounded-md h-14 items-centerl bg-cyan-800 border-cyan-900 border-b-4 border-r-2 border-l-2 border-t-2">
        <input
          type="file"
          accept="image/*"
          onChange={handleProfilePicChange}
          ref={fileInputRef}
          className="hidden"
        />
        <button
          onClick={handleClick}
          className="cursor-pointer text-white rounded-md  "
        >
        <h1 className="text-white font-bold">Edit Picture</h1>
        </button>
      </div>
    );
  };

  export const Button4 = ({ title, action, icon: Icon, color }) => {
    const [isPressed, setIsPressed] = useState(false);
  
    const handlePressStart = () => {
      setIsPressed(true);
    };
  
    const handlePressEnd = () => {
      setIsPressed(false);
    };
  
    return (
      <div
        className={`cursor-pointer flex justify-center p-3 rounded-md h-14 items-center ${
          isPressed
            ? 'bg-yellow-400 border-yellow-500 border-b-2 border-r-2 border-l-2 border-t-2'
            : 'bg-yellow-400 border-yellow-500 border-b-4 border-r-2 border-l-2 border-t-2'
        }`}
        onClick={action}
        onMouseDown={handlePressStart}
        onMouseUp={handlePressEnd}
        onMouseLeave={handlePressEnd}
        onTouchStart={handlePressStart}
        onTouchEnd={handlePressEnd}
      >
        <h1 className="text-white font-bold">{title}</h1>
        {Icon && <Icon className="ml-2 w-4 h-4 fill-white " />}
      </div>
    );
  };

export const GoogleButton = ({ title, action, saving }) => {
  const [isPressed, setIsPressed] = useState(false);

  const handlePressStart = () => {
    setIsPressed(true);
  };

  const handlePressEnd = () => {
    setIsPressed(false);
  };

  return (
    <div
      className={`cursor-pointer flex justify-center p-3 rounded-md h-14 items-center ${
        isPressed
          ? 'bg-white border-gray-300 flex justify-center p-3 gap-2 rounded-md border-b-2 border-r-2 border-l-2 border-t-2'
          : 'bg-white border-gray-300 flex justify-center p-3 gap-2 rounded-md border-b-4 border-r-2 border-l-2 border-t-2'
      }`}
      onClick={action}
      onMouseDown={handlePressStart}
      onMouseUp={handlePressEnd}
      onMouseLeave={handlePressEnd}
      onTouchStart={handlePressStart}
      onTouchEnd={handlePressEnd}
    >
      <img src={Google} className="h-6" alt="Google Logo" />
      <h1 className="text-black font-bold">{saving ? <LoadingSpinner/> : title }</h1>
    </div>
  );
};

export const TextButton = ({title, color, position, action}) => {
    return(
        <h1 onClick={action} className={`text-${color}  cursor-pointer text-${position} pt-2 {decoration}`}>{title}</h1>
    )
}

export const MenuButton = ({title, icon, active, url}) => {


  return(
    <a href={url}>
      <div className={`w-full flex gap-2 ${active ? 'bg-cyan-900 ' : 'transparent' }rounded-md p-4 items-center`}>
          {icon && (
            <div className="mr-2">
              {React.cloneElement(icon, { className: `${icon.props.className || ''} h-5 w-5 ${active ? 'fill-white' : 'fill-cyan-800' }` })}
            </div>
          )}
          
          <h1 className={`${active ? 'text-white' : 'text-cyan-800'} font-bold capitalize`}>{title}</h1>
      </div>
    </a>
  )

}