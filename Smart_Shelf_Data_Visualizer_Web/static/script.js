let isRunning = false;
let interval;
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const downloadBtn = document.getElementById('downloadBtn');
const statusText = document.getElementById('statusText');
const led = document.querySelector('.led');
const plotContainer = document.getElementById('plotContainer');

// Update plot image
const updatePlot = async () => {
    try {
        const response = await fetch('/plot');
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        plotContainer.innerHTML = `<img src="data:image/png;base64,${data.plot}" alt="Serial Data Plot">`;
    } catch (error) {
        console.error('Error updating plot:', error);
        plotContainer.innerHTML = '<p class="error">Error loading plot</p>';
    }
};

// Start data collection
startBtn.addEventListener('click', () => {
    if (!isRunning) {
        isRunning = true;
        led.classList.add('active');
        statusText.textContent = 'Connected';
        updatePlot();
        interval = setInterval(updatePlot, 1000);
    }
});

// Stop data collection
stopBtn.addEventListener('click', () => {
    isRunning = false;
    led.classList.remove('active');
    statusText.textContent = 'Disconnected';
    clearInterval(interval);
});

// Download CSV
downloadBtn.addEventListener('click', () => {
    window.location.href = '/download';
});