import React from "react";
import { Line } from "react-chartjs-2";

function LineChart({ chartData, selectedMonthIndex }) {
  // Validate selectedMonthIndex to prevent out-of-bound errors
  if (selectedMonthIndex < 0 || selectedMonthIndex >= 12) {
    return <div>No data available for selected month</div>;
  }

  // Determine the month string based on selectedMonthIndex (assuming 0 is January, 1 is February, ..., 11 is December)
  const selectedMonthString = `${selectedMonthIndex + 1}`.padStart(2, '0'); // Convert index to two-digit string (01, 02, ..., 12)

  // Filter chartData to get data for the selected month
  const selectedMonthData = chartData.filter((data) => data.date.startsWith(`2024-${selectedMonthString}`));

  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];


  // Extracting data from selected month data
  const days = selectedMonthData.map((data) => data.date.slice(8));
  const type1Data = selectedMonthData.map((data) => data.accidents.type1);
  const type2Data = selectedMonthData.map((data) => data.accidents.type2);
  const type3Data = selectedMonthData.map((data) => data.accidents.type3);
  const type4Data = selectedMonthData.map((data) => data.accidents.type4);

  const data = {
    labels: days,
    datasets: [
      {
        label: "Type 1 Severity",
        data: type1Data,
        borderColor: "rgba(253, 186, 116, 1)",
        backgroundColor: "rgba(253, 186, 116, 0.2)",
        borderWidth: 3,
        fill: true,
        tension: 0.5,
      },
      {
        label: "Type 2 Severity",
        data: type2Data,
        borderColor: "rgba(16, 185, 129, 1)",
        backgroundColor: "rgba(16, 185, 129, 0.2)",
        borderWidth: 3,
        fill: true,
        tension: 0.5,
      },
      {
        label: "Type 3 Severity",
        data: type3Data,
        borderColor: "rgba(252, 165, 165, 1)",
        backgroundColor: "rgba(252, 165, 165, 0.2)",
        borderWidth: 3,
        fill: true,
        tension: 0.5,
      }
    ],
  };

  return (
    <div className="chart-container p-3 bg-gray-50 rounded-lg mt-4">
      <h2 style={{ textAlign: "center" }} className="mb-5">Line Chart</h2>
      <Line
        data={data}
        options={{
          plugins: {
            title: {
              display: true,
              text: `Distribution of predicted accident severity over ${months[selectedMonthIndex]} 2024`,
            },
            legend: {
              display: true,
              position: "bottom",
            },
          },
          elements: {
            point: {
              radius: 2, // Hide points on lines
            },
          }
        }}
      />
    </div>
  );
}

export default LineChart;
