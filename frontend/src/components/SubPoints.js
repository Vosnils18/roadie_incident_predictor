import React from "react";

const SubPoints = ({available, text, dark}) => {
    return (
        <div className="flex gap-4 items-center">
            <div className={`${available ? 'bg-emerald-400 ' : 'bg-red-300 '} h-4 w-4 rounded-full`}></div>
            <h2 className={`${dark ? 'text-white' : 'text-gray-800'} text-md`}>{text}</h2>
        </div>
    )
}

export default SubPoints;