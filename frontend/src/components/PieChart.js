import React from "react";
import { Pie } from "react-chartjs-2";

function PieChart({ chartData, selectedMonthIndex }) {
  // Check if chartData exists and has at least one entry
  if (!chartData || chartData.length === 0) {
    return <div>No data available</div>; // Handle case where chartData is empty
  }

  // Filter chartData to get data for the selected month
  const selectedMonthData = chartData.filter((data) => {
    const date = new Date(data.date);
    return date.getMonth() === selectedMonthIndex;
  });

  // Aggregate total accidents for the selected month
  const totalAccidents = selectedMonthData.reduce((acc, curr) => {
    acc.type1 += curr.accidents.type1 || 0;
    acc.type2 += curr.accidents.type2 || 0;
    acc.type3 += curr.accidents.type3 || 0;
    acc.type4 += curr.accidents.type4 || 0;
    return acc;
  }, { type1: 0, type2: 0, type3: 0, type4: 0 });

  // Extracting labels and data for the Pie chart
  const labels = Object.keys(totalAccidents);
  const data = Object.values(totalAccidents);

  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const selectedMonthLabel = months[selectedMonthIndex];

  const chartDataConfig = {
    labels: labels,
    datasets: [
      {
        label: `Accident Severity Distribution - ${selectedMonthLabel}`,
        data: data,
        backgroundColor: [
          "rgba(253, 186, 116, 0.6)", // Adjust colors as needed
          "rgba(16, 185, 129, 0.6)",
          "rgba(252, 165, 165, 0.6)",
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="chart-container p-3 bg-gray-50 rounded-lg mt-4">
      <h2 style={{ textAlign: "center" }} className="mb-5">Pie Chart</h2>
      <Pie
        data={chartDataConfig}
        options={{
          plugins: {
            title: {
              display: true,
              text: `Distribution of predicted accident severity over ${months[selectedMonthIndex]} 2024`,
            },
            legend: {
              display: false,
              position: "top",
            },
          },
        }}
      />
    </div>
  );
}

export default PieChart;
