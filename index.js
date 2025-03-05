document.addEventListener("DOMContentLoaded", function() {
    // Date selection functionality
    const dateBox = document.getElementById("date-box");
    const dateBoxText = document.getElementById("date-box-text");
    const dateInputs = document.getElementById("date-inputs");
    const startDate = document.getElementById("start-date");
    const endDate = document.getElementById("end-date");

    // Function to toggle date input popup
    function toggleDateInputs(event) {
        event.stopPropagation(); // Prevents event from bubbling up
        dateBox.classList.add("expanded"); // Ensure expanded mode
        dateInputs.classList.remove("hidden"); // Show date inputs
        dateBoxText.classList.add("hidden"); // Hide button text
        document.body.classList.add("blur");
    }

    // Function to close the date input popup
    function closeDateInputs() {
        dateBox.classList.remove("expanded");
        dateInputs.classList.add("hidden");
        dateBoxText.classList.remove("hidden");
        document.body.classList.remove("blur");
    }

    // Prevent popup from closing when clicking inside the date inputs
    dateInputs.addEventListener("click", function(event) {
        event.stopPropagation();
    });

    // Allow proper focus and selection for date pickers
    startDate.addEventListener("focus", function(event) {
        event.stopPropagation(); // Prevents event from closing popup
    });

    endDate.addEventListener("focus", function(event) {
        event.stopPropagation();
    });

    startDate.addEventListener("click", function(event) {
        event.stopPropagation();
    });

    endDate.addEventListener("click", function(event) {
        event.stopPropagation();
    });

    // Automatically close popup when both dates are selected
    function checkAndSubmitDates() {
        if (startDate.value && endDate.value) {
            console.log("Start Date:", startDate.value, "End Date:", endDate.value);
            closeDateInputs(); // Close popup after both dates are selected
        }
    }

    startDate.addEventListener("change", checkAndSubmitDates);
    endDate.addEventListener("change", checkAndSubmitDates);

    // Ensure that clicking anywhere outside the date input closes it
    document.addEventListener("click", function() {
        if (dateBox.classList.contains("expanded")) {
            closeDateInputs();
        }
    });

    // Ensure clicking the date box itself opens the popup
    dateBox.addEventListener("click", function(event) {
        toggleDateInputs(event);
    });
});
