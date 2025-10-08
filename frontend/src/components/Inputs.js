import React, { useState, useEffect, useRef } from "react";


export const Input = ({ icon, placeholder, value, setValue }) => {
  const [selected, setSelected] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    // Function to handle clicks outside the component
    const handleClickOutside = (event) => {
      if (inputRef.current && !inputRef.current.contains(event.target)) {
        setSelected(false);
      }
    };

    // Attach event listener when the component mounts
    document.addEventListener("click", handleClickOutside);

    // Remove event listener when the component unmounts
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  return (
    <div
      className={`flex flex-row border-b-2 p-3 gap-5 my-2 ${
        selected ? "border-cyan-500" : "border-cyan-900"
      } `}
      onClick={() => {
        setSelected(!selected);
      }}
    >
      <div className="fill-current mr-2">
      {icon && (
        <div className="mr-2">
          {React.cloneElement(icon, { className: `${icon.props.className || ''} h-5 w-5 ${selected ? 'fill-cyan-500' : 'fill-cyan-900' }` })}
        </div>
      )}
      </div>
      <input
        ref={inputRef}
        type="text"
        className={`bg-transparent focus:outline-none ${selected ? "text-cyan-500 placeholder-cyan-500" : "text-cyan-900 placeholder-cyan-900"}`}
        placeholder={placeholder}
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
    </div>
  );
};

export const PasswordInput = ({ icon, placeholder, value, setValue }) => {
    const [selected, setSelected] = useState(false);
    const inputRef = useRef(null);
  
    useEffect(() => {
      // Function to handle clicks outside the component
      const handleClickOutside = (event) => {
        if (inputRef.current && !inputRef.current.contains(event.target)) {
          setSelected(false);
        }
      };
  
      // Attach event listener when the component mounts
      document.addEventListener("click", handleClickOutside);
  
      // Remove event listener when the component unmounts
      return () => {
        document.removeEventListener("click", handleClickOutside);
      };
    }, []);
  
    return (
      <div
        className={`flex flex-row border-b-2 p-3 my-2 gap-5 ${
          selected ? "border-cyan-500" : "border-cyan-900"
        } `}
        onClick={() => {
          setSelected(!selected);
        }}
      >
        {icon && (
          <div className="mr-2">
            {React.cloneElement(icon, { className: `${icon.props.className || ''} h-5 w-5 ${selected ? 'fill-cyan-500' : 'fill-cyan-900' }` })}
          </div>
        )}
        <input
          ref={inputRef}
          type={selected ? "text" : "password"}
          className={`bg-transparent focus:outline-none ${selected ? "text-cyan-500 placeholder-cyan-500" : "text-cyan-900 placeholder-cyan-900"}`}
          placeholder={placeholder}
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
      </div>
    );
  };

export const List = ({ icon, placeholder, value, setValue, options }) => {
  const [selected, setSelected] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    // Function to handle clicks outside the component
    const handleClickOutside = (event) => {
      if (inputRef.current && !inputRef.current.contains(event.target)) {
        setSelected(false);
      }
    };

    // Attach event listener when the component mounts
    document.addEventListener("click", handleClickOutside);

    // Remove event listener when the component unmounts
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  return (
    <div
      className={`relative border-b-2 p-3 gap-5 my-2 ${
        selected ? "border-cyan-500" : "border-cyan-900"
      } `}
      onClick={() => {
        setSelected(!selected);
      }}
    >
      <div className="flex flex-row items-center gap-5">
        <div className="mr-2">
          {icon && (
            <div>
              {React.cloneElement(icon, {
                className: `${icon.props.className || ""} h-5 w-5 ${
                  selected ? "fill-cyan-500" : "fill-cyan-900"
                }`,
              })}
            </div>
          )}
        </div>
        <input
          ref={inputRef}
          type="text"
          className={`bg-transparent focus:outline-none w-full ${
            selected ? "text-cyan-500 placeholder-cyan-500" : "text-cyan-900 placeholder-cyan-900"
          }`}
          placeholder={placeholder}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          readOnly
        />
        <p className="text-gray-400">km</p>
      </div>
      {selected && (
        <div className="absolute w-full mt-1 py-1 bg-white border border-gray-300 rounded shadow-md z-10">
          {options.map((option) => (
            <div
              key={option.value}
              className="cursor-pointer px-4 py-2 hover:bg-gray-100"
              onClick={() => {
                setValue(option.value);
                setSelected(false);
              }}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};