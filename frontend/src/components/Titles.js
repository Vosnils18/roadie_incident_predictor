import React from "react";

export const TitleWithSubtitle = ({ title, subtitle, color, span }) => {
    const titleColorClass = color === 2 ? 'text-gray-800' : 'text-white';
    const subtitleColorClass = color === 2 ? 'text-gray-500' : 'text-cyan-600';

    return (
        <div className="z-0">
            <h1 className={`text-3xl font-semibold mb-2 ${titleColorClass}`}>{title} <span className={`text-lg mb-2 text-emerald-400 `}>{span}</span></h1>
            <h3 className={subtitleColorClass}>{subtitle}</h3>
        </div>
    );
};


export const SectionTitle = ({title}) => {
    return(
        <h1 className="text-gray-800 text-2xl font-semibold">{title}</h1>
    )
}

export const SectionTitleSmall = ({title}) => {
    return(
        <h1 className="text-gray-500 text-l font-semibold">{title}</h1>
    )
}

export const ColoredTitle = ({ segments, subtitle }) => {
    return (
        <>
        <h1 className="text-3xl font-semibold">
            {segments.map((segment, index) => (
                <span key={index} className={segment.colorClass}>
                    {segment.text}
                </span>
            ))}
        </h1>
        <h3 className="text-emerald-500 mt-5">{subtitle}</h3>
        </>
    );
};