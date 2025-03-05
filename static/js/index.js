document.addEventListener("DOMContentLoaded", function() {
    // Ensure the input field exists before applying event listeners
    const inputField = document.querySelector(".input-section input");
    if (inputField) {
        inputField.addEventListener("focus", function() {
            inputField.style.borderColor = "#f08080";
        });
        inputField.addEventListener("blur", function() {
            inputField.style.borderColor = "#fff";
        });
    }

    // Ensure healthBoxes exist before applying event listeners
    const healthBoxes = document.querySelectorAll(".health-box");
    if (healthBoxes.length > 0) {
        healthBoxes.forEach(box => {
            box.addEventListener("mouseover", function() {
                box.style.boxShadow = "5px 5px 15px rgba(0,0,0,0.3)";
            });
            box.addEventListener("mouseout", function() {
                box.style.boxShadow = "2px 2px 10px rgba(0,0,0,0.2)";
            });
        });
    }
});

// Function to toggle date input popup
function toggleDateInputs(event) {
    event.stopPropagation();
    const dateBox = document.getElementById('date-box');
    const dateBoxText = document.getElementById('date-box-text');
    const dateInputs = document.getElementById('date-inputs');

    // Toggle the expanded class for popup size increase
    dateBox.classList.toggle('expanded');
    dateInputs.classList.toggle('hidden');
    dateBoxText.classList.toggle('hidden');

    // Apply blur effect only to the container
    if (dateBox.classList.contains('expanded')) {
        document.body.classList.add('blur');
    } else {
        document.body.classList.remove('blur');
    }
}

// Function to close the date input popup
function closeDateInputs(event) {
    event.stopPropagation();
    const dateBox = document.getElementById('date-box');
    const dateBoxText = document.getElementById('date-box-text');
    const dateInputs = document.getElementById('date-inputs');

    dateBox.classList.remove('expanded');
    dateInputs.classList.add('hidden');
    dateBoxText.classList.remove('hidden');

    // Remove the blur effect when popup is closed
    document.body.classList.remove('blur');
}