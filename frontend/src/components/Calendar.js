import React, { useState, useEffect } from 'react';
import { ReactComponent as AngleIcon } from '../assets/icons/angle.svg';

const CalendarStrip = ({setSelectedMonthIndex}) => {
  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth());
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());

  const handlePrevMonth = () => {
    setSelectedMonth(prevMonth => (prevMonth - 1 + 12) % 12);
    if (selectedMonth === 0) {
      setSelectedYear(prevYear => prevYear - 1);
    }
  };

  const handleNextMonth = () => {
    setSelectedMonth(prevMonth => (prevMonth + 1) % 12);
    if (selectedMonth === 11) {
      setSelectedYear(prevYear => prevYear + 1);
    }
  };

  useEffect(() => {
    setSelectedMonth(new Date().getMonth());
    setSelectedYear(new Date().getFullYear());
  }, []);

  useEffect(() => {
    setSelectedMonthIndex(selectedMonth);
  }, [selectedMonth]);

  return (
    <div className='w-full max-w-3xl mx-auto h-40'>
      <div className='bg-gray-100 p-3 rounded-lg flex justify-between items-center'>
        <AngleIcon className="h-5 w-5 cursor-pointer fill-gray-800" onClick={handlePrevMonth} />
        <h1 className='text-xl font-bold'>{months[selectedMonth]} {selectedYear}</h1>
        <AngleIcon className="h-5 w-5 rotate-180 cursor-pointer fill-gray-800" onClick={handleNextMonth} />
      </div>
      <div className='grid grid-cols-6 gap-2 mt-4 h-16'>
        {months.map((month, index) => (
          <div
            key={index}
            className={`h-10 flex flex-col items-center cursor-pointer p-2 border-x-2 border-t-2 border-b-4 ${index === selectedMonth ? 'bg-cyan-900 text-white rounded-md border-cyan-950' : 'border-white'}`}
            onClick={() => setSelectedMonth(index)}
          >
            <span className={`text-sm ${index === selectedMonth ? 'text-cyan-200' : 'text-gray-500'}`}>{month.substring(0, 3)}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CalendarStrip;
