document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.querySelector(".input-section input");
    inputField.addEventListener("focus", function() {
        inputField.style.borderColor = "#f08080";
    });
    inputField.addEventListener("blur", function() {
        inputField.style.borderColor = "#fff";
    });
    
    const healthBoxes = document.querySelectorAll(".health-box");
    healthBoxes.forEach(box => {
        box.addEventListener("mouseover", function() {
            box.style.boxShadow = "5px 5px 15px rgba(0,0,0,0.3)";
        });
        box.addEventListener("mouseout", function() {
            box.style.boxShadow = "2px 2px 10px rgba(0,0,0,0.2)";
        });
    });
});

function toggleDateInputs() {
    const dateBox = document.getElementById('date-box');
    const dateBoxText = document.getElementById('date-box-text');
    const dateInputs = document.getElementById('date-inputs');
    dateBox.classList.toggle('expanded');
    dateInputs.classList.toggle('hidden');
    dateBoxText.classList.toggle('hidden');
}