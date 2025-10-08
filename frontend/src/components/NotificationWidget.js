import React from "react";

const NotificationWidget = ({  body, level, date }) => {
  // Define colors based on the level
  const levelColors = {
    Low: 'bg-green-300',
    Medium: 'bg-orange-300',
    High: 'bg-red-300',
  };

  return (
    <div className="bg-gray-100 p-3 rounded-lg w-full flex gap-5 items-center">
      {/* Use dynamic class for the circle based on the level */}
      <div className={`h-10 w-12 rounded-full ${levelColors[level]}`}></div>
      <div className="w-full">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-gray-800 font-bold text-xl capitalize">{level}</h2>
          <h2 className="text-gray-400 text-l">{date}</h2>
        </div>
        <h2 className="text-gray-600 text-l">{body}</h2>
      </div>
    </div>
  );
}

export default NotificationWidget;
