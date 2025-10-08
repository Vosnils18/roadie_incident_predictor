import React, { useState } from "react";
import { SectionTitle, SectionTitleSmall } from "./Titles";
import Gap from "./Gap";

import { ReactComponent as SpeedIcon } from '../assets/icons/tachometer-alt-fastest.svg';
import { ReactComponent as BrakingIcon } from '../assets/icons/stop.svg';
import { ReactComponent as CorneringIcon } from '../assets/icons/diamond-turn-right.svg';
import { ReactComponent as ArrowIcon } from '../assets/icons/angle.svg';
import { ReactComponent as CloseIcon } from '../assets/icons/close.svg';

const Details = ({setDetails}) => {

    const handleClose = () => {
        setDetails(false);
    }

    const userWidget = (color, Icon, title, data) => {
        return (
            <div className={`p-2 px-3 rounded-lg bg-${color === 'emerald' ? color + '-400' : color + '-300'} flex gap-2`}>
                <div className="flex items-center">
                    <Icon className="w-6 h-6 mr-2 fill-white" />
                </div>
                <div>
                    <h1 className="text-lg text-white font-bold">{title}</h1>
                    <p className={`text-${color}-500`}>{data}</p>
                </div>
            </div>
        );
    };

    const useToggle = (initialState) => {
        const [isOpen, setIsOpen] = useState(initialState);
        const toggle = () => setIsOpen(!isOpen);
        return [isOpen, toggle];
    };

    const IncidentType = ({ name, probability, severity, description, open }) => {
        const [isOpen, toggle] = useToggle(open);

        return (
            <div className="bg-gray-100 p-4 rounded-lg cursor-pointer" onClick={toggle}> 
                <div className="flex justify-between items-center">
                    <div>
                        <h1 className="text-lg font-bold text-gray-700 mb-3">{name}</h1>
                        <div className="flex gap-2 items-center">
                            <div className="p-1 px-2 bg-cyan-950 rounded-md">
                                <p className="text-white font-bold">{probability} %</p>
                            </div>
                            <div className={`p-1 px-2 bg-${severity === 'Low' ? 'emerald-400' : severity === 'Medium' ? 'orange-300' : severity === 'High' ? 'red-300' : 'gray-400' } rounded-md`}>
                                <p className="text-white font-bold">{severity}</p>
                            </div>
                        </div>
                    </div>
                        <ArrowIcon className={`w-5 h-5 mr-2 fill-gray-400 ${isOpen ? 'rotate-90' : '-rotate-90'}`} />
                </div>
                {isOpen && <p className="text-gray-500 mt-4">{description}</p>}
            </div>
        );
    };

    return (
        <div>
            <div className="flex justify-between gap-5">
                <div>
                    <SectionTitle title={'Predictions'} />
                    <SectionTitleSmall title={'Johan Willem Frisolaan 27-15, 4835 AA Breda'} />
                </div>
                <CloseIcon className="w-8 h-8 fill-gray-800" onClick={handleClose}></CloseIcon>
            </div>
            <Gap />

            <SectionTitleSmall title={'User'} />
            <Gap /> 
            <div className="flex gap-2 flex-wrap">
                {userWidget('emerald', SpeedIcon, 'Speed', '120 km/h')}
                {userWidget('orange', BrakingIcon, 'Braking', '12 m/s')}
                {userWidget('red', CorneringIcon, 'Cornering', 'N / A')}
            </div>
            <Gap />
            <SectionTitleSmall title={'Probabilities'} />
            <Gap />
            <div className="flex flex-col gap-4">
                <IncidentType
                    name='Speeding'
                    probability='90'
                    severity='High'
                    description='The likelihood of an accident is significantly increased, with speeding presenting the highest risk. Consider slowing down or seeking an alternate route to minimize the risk of accidents.'
                    open={false}
                />
                <IncidentType
                    name='Harsh Breaking'
                    probability='56'
                    severity='Medium'
                    description='The likelihood of an accident is significantly increased, with speeding presenting the highest risk. Consider slowing down or seeking an alternate route to minimize the risk of accidents.'
                    open={false}
                />
                <IncidentType
                    name='Harsh Corneling'
                    probability='39'
                    severity='Low'
                    description='The likelihood of an accident is significantly increased, with speeding presenting the highest risk. Consider slowing down or seeking an alternate route to minimize the risk of accidents.'
                    open={false}
                />
                <IncidentType
                    name='Accelerating'
                    probability='91'
                    severity='High'
                    description='The likelihood of an accident is significantly increased, with speeding presenting the highest risk. Consider slowing down or seeking an alternate route to minimize the risk of accidents.'
                    open={false}
                />
            </div>
            <Gap></Gap>
        </div>
    );
};

export default Details;
