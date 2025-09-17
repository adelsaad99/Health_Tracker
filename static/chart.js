// Wait until the page is fully loaded
document.addEventListener("DOMContentLoaded", function() {
// Get the canvas element where the chart will be drawn
const ctx = document.getElementById('healthChart').getContext('2d');

// Create a new chart with Chart.js
const healthChart = new Chart(ctx, {
type: 'line', // Set chart type to line
data: {
labels: window.healthData.dates, // Use dates as labels
datasets: [
// Exercise dataset
{
label: 'Exercise (min)', // Label for exercise
data: window.healthData.exercise_data, // Exercise data values
borderColor: 'rgba(54, 162, 235, 1)', // Line color
backgroundColor: 'rgba(54, 162, 235, 0.2)', // Fill color
tension: 0.3, // Curve smoothness
pointBackgroundColor: 'rgba(54, 162, 235, 1)', // Point color
pointRadius: 5 // Point size
},
// Meditation dataset
{
label: 'Meditation (min)', // Label for meditation
data: window.healthData.meditation_data, // Meditation data values
borderColor: 'rgba(255, 206, 86, 1)', // Line color
backgroundColor: 'rgba(255, 206, 86, 0.2)', // Fill color
tension: 0.3, // Curve smoothness
pointBackgroundColor: 'rgba(255, 206, 86, 1)', // Point color
pointRadius: 5 // Point size
},
// Sleep dataset
{
label: 'Sleep (hours)', // Label for sleep
data: window.healthData.sleep_data, // Sleep data values
borderColor: 'rgba(153, 102, 255, 1)', // Line color
backgroundColor: 'rgba(153, 102, 255, 0.2)', // Fill color
tension: 0.3, // Curve smoothness
pointBackgroundColor: 'rgba(153, 102, 255, 1)', // Point color
pointRadius: 5 // Point size
}
]
},
options: {
responsive: true, // Make chart responsive
plugins: {
// Tooltip settings
tooltip: {
mode: 'index', // Show all values at index
intersect: false, // No need to hover exactly
titleFont: { size: 16, weight: 'bold' }, // Tooltip title font
bodyFont: { size: 14 }, // Tooltip body font
},
// Legend settings
legend: {
labels: { font: { size: 14 } } // Legend font size
}
},
// Interaction settings
interaction: {
mode: 'nearest', // Show nearest point
axis: 'x', // Interaction on X axis
intersect: false // No need to hover exactly
},
// Scale settings
scales: {
y: { beginAtZero: true, ticks: { font: { size: 14 } } }, // Y axis starts at zero
x: { ticks: { font: { size: 14 } } } // X axis font size
}
}
});
});
