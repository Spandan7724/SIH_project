/*
// Update progress bar based on current frame being processed
function updateProgressBar(progressPercentage) {
    console.log('Updating progress bar with percentage: ' + progressPercentage);

    // Simulate progress reaching 99% over 40 seconds
    if (progressPercentage < 99) {
        setTimeout(function () {
            $('#progress-bar').css('width', progressPercentage + '%').attr('aria-valuenow', progressPercentage);
            updateProgressBar(progressPercentage + 1); // Increment progress by 1%
        }, 400); // Update every 400 milliseconds (0.4 seconds) until 99%
    } else {
        // Stay at 99% until result.html page loads
        setTimeout(function () {
            window.location.href = "/result"; // Redirect to the result page
        }, 5000); // Stay at 99% for an additional 60 seconds (total of 61 seconds)
    }
}

// Start updating progress bar when upload button is clicked
$('#uploadForm').on('submit', function (event) {
    event.preventDefault(); // Prevent form submission

    // Show progress container
    $('#progress-container').show();

    // Start updating progress bar
    updateProgressBar(1);
});
*/
const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

let interval = null;

document.addEventListener('DOMContentLoaded', function () {
    const cornerTextElement = document.querySelector(".corner-text");

    if (cornerTextElement) {
        cornerTextElement.onmouseover = event => {
            let iteration = 0;

            clearInterval(interval);

            interval = setInterval(() => {
                event.target.innerText = event.target.innerText
                    .split("")
                    .map((letter, index) => {
                        if (index < iteration) {
                            return event.target.dataset.value[index];
                        }

                        return letters[Math.floor(Math.random() * 26)];
                    })
                    .join("");

                if (iteration >= event.target.dataset.value.length) {
                    clearInterval(interval);
                }

                iteration += 1 / 3;
            }, 20); //to adjust the speed of the animation
        };
    } else {
        console.error("Element with class 'corner-text' not found.");
    }
});
