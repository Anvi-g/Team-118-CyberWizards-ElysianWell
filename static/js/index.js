document.addEventListener("DOMContentLoaded", function() {
    const healthBoxes = document.querySelectorAll(".health-box");
    healthBoxes.forEach(box => {
        box.addEventListener("mouseover", function() {
            box.style.boxShadow = "5px 5px 15px rgba(0,0,0,0.3)";
        });
        box.addEventListener("mouseout", function() {
            box.style.boxShadow = "2px 2px 10px rgba(0,0,0,0.2)";
        });
    });

    document.getElementById("end-date").addEventListener("change", calculateCycle);
});

function toggleCalendar(event) {
    event.stopPropagation();
    document.getElementById("calendar-popup").classList.toggle("hidden");
}

function closeCalendar(event) {
    event.stopPropagation();
    document.getElementById("calendar-popup").classList.add("hidden");
}

function calculateCycle() {
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;

    if (startDate && endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        const cycleLength = Math.round((end - start) / (1000 * 60 * 60 * 24));
        
        const nextPeriodStart = new Date(end);
        nextPeriodStart.setDate(nextPeriodStart.getDate() + cycleLength);
        displayPrediction(nextPeriodStart, cycleLength);
    }
}

function displayPrediction(nextPeriodDate, cycleLength) {
    let predictionBox = document.getElementById("prediction-box");

    predictionBox.innerHTML = `
        <strong>Predicted Next Period Start:</strong> ${nextPeriodDate.toDateString()}<br>
        <strong>Cycle Length:</strong> ${cycleLength} days
    `;
    showDialog();
}

function showDialog() {
    document.getElementById("prediction-dialog").classList.add("show");
}

function closeDialog() {
    document.getElementById("prediction-dialog").classList.remove("show");
}
