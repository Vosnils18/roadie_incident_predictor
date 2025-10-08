import React, { useEffect } from "react";
import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import { useState } from "react";

//Components
import CalendarStrip from "../components/Calendar";
import { SectionTitleSmall } from "../components/Titles";
import Gap from "../components/Gap";
import LineChart from "../components/LineChart";
import PieChart from "../components/PieChart";

Chart.register(CategoryScale);

const Statistics = () => {

    const [selectedMonthIndex, setSelectedMonthIndex] = useState(new Date()); // Initial selected month index

    const Data = [
      {
          id: 1,
          date: '2024-06-01',
          accidents: {
              type1: 2,
              type2: 1,
              type3: 3,
          },
      },
      {
          id: 2,
          date: '2024-06-02',
          accidents: {
              type1: 0,
              type2: 1,
              type3: 2,
          },
      },
      {
          id: 3,
          date: '2024-06-03',
          accidents: {
              type1: 1,
              type2: 2,
              type3: 1,
          },
      },
      {
          id: 4,
          date: '2024-06-04',
          accidents: {
              type1: 2,
              type2: 0,
              type3: 3,
          },
      },
      {
          id: 5,
          date: '2024-06-05',
          accidents: {
              type1: 1,
              type2: 3,
              type3: 0,
          },
      },
      {
          id: 6,
          date: '2024-06-06',
          accidents: {
              type1: 3,
              type2: 1,
              type3: 1,
          },
      },
      {
          id: 7,
          date: '2024-06-07',
          accidents: {
              type1: 0,
              type2: 2,
              type3: 2,
          },
      },
      {
          id: 8,
          date: '2024-06-08',
          accidents: {
              type1: 2,
              type2: 1,
              type3: 0,
          },
      },
      {
          id: 9,
          date: '2024-06-09',
          accidents: {
              type1: 1,
              type2: 0,
              type3: 3,
          },
      },
      {
          id: 10,
          date: '2024-06-10',
          accidents: {
              type1: 2,
              type2: 2,
              type3: 1,
          },
      },
      {
          id: 11,
          date: '2024-06-11',
          accidents: {
              type1: 0,
              type2: 1,
              type3: 2,
          },
      },
      {
          id: 12,
          date: '2024-06-12',
          accidents: {
              type1: 3,
              type2: 0,
              type3: 1,
          },
      },
      {
          id: 13,
          date: '2024-06-13',
          accidents: {
              type1: 1,
              type2: 2,
              type3: 0,
          },
      },
      {
          id: 14,
          date: '2024-06-14',
          accidents: {
              type1: 2,
              type2: 1,
              type3: 1,
          },
      },
      {
          id: 15,
          date: '2024-06-15',
          accidents: {
              type1: 1,
              type2: 2,
              type3: 1,
          },
      },
      {
          id: 16,
          date: '2024-06-16',
          accidents: {
              type1: 0,
              type2: 1,
              type3: 3,
          },
      },
      {
          id: 17,
          date: '2024-06-17',
          accidents: {
              type1: 2,
              type2: 1,
              type3: 0,
          },
      },
      {
          id: 18,
          date: '2024-06-18',
          accidents: {
              type1: 1,
              type2: 0,
              type3: 2,
          },
      },
      {
          id: 19,
          date: '2024-06-19',
          accidents: {
              type1: 3,
              type2: 2,
              type3: 1,
          },
      },
      {
          id: 20,
          date: '2024-06-20',
          accidents: {
              type1: 0,
              type2: 3,
              type3: 0,
          },
      },
      {
          id: 21,
          date: '2024-06-21',
          accidents: {
              type1: 2,
              type2: 1,
              type3: 1,
          },
      },
      {
          id: 22,
          date: '2024-06-22',
          accidents: {
              type1: 1,
              type2: 0,
              type3: 2,
          },
      },
      {
          id: 23,
          date: '2024-06-23',
          accidents: {
              type1: 3,
              type2: 2,
              type3: 0,
          },
      },
      {
          id: 24,
          date: '2024-06-24',
          accidents: {
              type1: 0,
              type2: 1,
              type3: 3,
          },
      },
      {
          id: 25,
          date: '2024-06-25',
          accidents: {
              type1: 2,
              type2: 0,
              type3: 1,
          },
      },
      {
          id: 26,
          date: '2024-06-26',
          accidents: {
              type1: 1,
              type2: 2,
              type3: 2,
          },
      },
      {
          id: 27,
          date: '2024-07-01',
          accidents: {
              type1: 0,
              type2: 3,
              type3: 1,
          },
      },
      {
          id: 28,
          date: '2024-07-02',
          accidents: {
              type1: 3,
              type2: 1,
              type3: 0,
          },
      },
      // Extra dummy data
      {
          id: 29,
          date: '2024-07-03',
          accidents: {
              type1: 1,
              type2: 2,
              type3: 2,
          },
      },
      {
          id: 30,
          date: '2024-07-04',
          accidents: {
              type1: 2,
              type2: 0,
              type3: 3,
          },
      },
      {
          id: 31,
          date: '2024-07-05',
          accidents: {
              type1: 0,
              type2: 1,
              type3: 0,
          },
      },
      {
          id: 32,
          date: '2024-07-06',
          accidents: {
              type1: 3,
              type2: 2,
              type3: 1,
          },
      },
      {
          id: 33,
          date: '2024-07-07',
          accidents: {
              type1: 1,
              type2: 0,
              type3: 2,
          },
      },
      {
          id: 34,
          date: '2024-08-01',
          accidents: {
              type1: 0,
              type2: 3,
              type3: 1,
          },
      },
      {
          id: 35,
          date: '2024-08-02',
          accidents: {
              type1: 2,
              type2: 1,
              type3: 0,
          },
      },
      {
          id: 36,
          date: '2024-08-03',
          accidents: {
              type1: 3,
              type2: 0,
              type3: 2,
          },
      },
      {
          id: 37,
          date: '2024-08-04',
          accidents: {
              type1: 1,
              type2: 2,
              type3: 3,
          },
      },
      {
          id: 38,
          date: '2024-08-05',
          accidents: {
              type1: 2,
              type2: 0,
              type3: 1,
          },
      },
      {
          id: 39,
          date: '2024-08-06',
          accidents: {
              type1: 0,
              type2: 1,
              type3: 2,
          },
      },
      {
          id: 40,
          date: '2024-08-07',
          accidents: {
              type1: 3,
              type2: 2,
              type3: 0,
          },
      },
      {
          id: 41,
          date: '2024-08-08',
          accidents: {
              type1: 1,
              type2: 0,
              type3: 3,
          },
      },
      {
          id: 42,
          date: '2024-08-09',
          accidents: {
              type1: 2,
              type2: 1,
              type3: 1,
          },
      },
      {
          id: 43,
          date: '2024-08-10',
          accidents: {
              type1: 0,
              type2: 2,
              type3: 0,
          },
      },
      {
          id: 44,
          date: '2024-08-11',
          accidents: {
              type1: 3,
              type2: 0,
              type3: 2,
          },
      },
      {
          id: 45,
          date: '2024-08-12',
          accidents: {
              type1: 1,
              type2: 2,
              type3: 1,
          },
      },
  ];
  
      

    return(
        <div className="p-5 bg-white h-full min-h-screen">
            <div className="mt-20 max-w-screen-md mx-auto">
                <CalendarStrip setSelectedMonthIndex={setSelectedMonthIndex}></CalendarStrip>
                <Gap></Gap>
                <SectionTitleSmall title={'Plots'}></SectionTitleSmall>
                <LineChart chartData={Data} selectedMonthIndex={selectedMonthIndex} />
                <PieChart chartData={Data} selectedMonthIndex={selectedMonthIndex} />
            </div>
        </div>
    )
}

export default Statistics