// Email Spam Classifier interactive features

// Loading animation with enhanced visual feedback
function showLoading() {
  const loadingIndicator = document.getElementById("loadingIndicator");
  const submitBtn = document.querySelector(".submit-btn");

  // Show loading indicator with fade-in effect
  loadingIndicator.style.display = "block";
  loadingIndicator.style.opacity = "0";
  setTimeout(() => {
    loadingIndicator.style.opacity = "1";
    loadingIndicator.style.transition = "opacity 0.3s";
  }, 10);

  // Disable submit button
  submitBtn.disabled = true;

  // Update progress steps with active class and animation
  const steps = document.querySelectorAll(".progress-step");
  steps[0].classList.add("active"); // Input step (should already be active)

  // Add animation to the Analysis step
  setTimeout(() => {
    steps[1].classList.add("active"); // Analysis step
  }, 300);
}

// Example emails
function fillExampleEmail(type) {
  let content = "";
  if (type === "spam") {
    content =
      "CONGRATULATIONS! You've been selected to receive a FREE $1000 Walmart gift card! Click here to claim now: http://claim-your-gift.com Limited time offer, ACT NOW!";
  } else {
    content =
      "Dear Team,\n\nPlease find attached the meeting notes from yesterday's planning session. Let me know if you need any clarification.\n\nRegards,\nJohn";
  }
  document.getElementById("email").value = content;

  // Update character count if counter exists
  const charCounter = document.getElementById("charCounter");
  if (charCounter) {
    const count = document.getElementById("email").value.length;
    charCounter.textContent =
      count + (count === 1 ? " character" : " characters");

    if (count > 200) {
      charCounter.style.color = "#dc3545";
    } else {
      charCounter.style.color = "#6c757d";
    }
  }
}

// Function to copy results to clipboard
function copyResultsToClipboard() {
  // Get the prediction result
  const isPredictionSpam =
    document.querySelector(".spam-indicator.spam") !== null;
  const predictionText = isPredictionSpam
    ? "SPAM DETECTED"
    : "LEGITIMATE EMAIL";

  // Get the confidence scores
  const spamConfidence = document
    .getElementById("spamConfidenceText")
    .textContent.trim();
  const notSpamConfidence = document
    .getElementById("notSpamConfidenceText")
    .textContent.trim();

  // Get the analyzed text
  const analyzedText = document.querySelector(".email-text").textContent.trim();

  // Create the text to copy
  const textToCopy = `Email Analysis Results:
---------------------
Verdict: ${predictionText}
Spam Likelihood: ${spamConfidence}
Legitimate Email Likelihood: ${notSpamConfidence}
---------------------
Analyzed Text:
${analyzedText}
---------------------
Analyzed with Advanced Email Spam Detector`;

  // Copy to clipboard
  navigator.clipboard
    .writeText(textToCopy)
    .then(() => {
      // Show toast if it exists
      const toastElement = document.getElementById("toastMessage");
      if (toastElement) {
        const toastBody = toastElement.querySelector(".toast-body");
        if (toastBody) {
          toastBody.textContent = "Results copied to clipboard!";
          const toast = new bootstrap.Toast(toastElement);
          toast.show();
        }
      } else {
        alert("Results copied to clipboard!");
      }
    })
    .catch((err) => {
      console.error("Error copying text: ", err);
      alert("Failed to copy results. Please try again.");
    });
}

// Character counter
function updateCharCount() {
  const textarea = document.getElementById("email");
  const charCounter = document.getElementById("charCounter");
  const count = textarea.value.length;

  charCounter.textContent =
    count + (count === 1 ? " character" : " characters");

  if (count > 200) {
    charCounter.style.color = "#dc3545";
  } else {
    charCounter.style.color = "#6c757d";
  }
}

// Toggle dark/light mode
function toggleTheme() {
  document.body.classList.toggle("dark-mode");
  const icon = document.getElementById("themeIcon");
  if (document.body.classList.contains("dark-mode")) {
    icon.classList.replace("bi-moon-fill", "bi-sun-fill");
    localStorage.setItem("theme", "dark");
  } else {
    icon.classList.replace("bi-sun-fill", "bi-moon-fill");
    localStorage.setItem("theme", "light");
  }
}

// Initialize theme from localStorage
function initTheme() {
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
    const icon = document.getElementById("themeIcon");
    if (icon) {
      icon.classList.replace("bi-moon-fill", "bi-sun-fill");
    }
  }
}

// Initialize tooltips
function initTooltips() {
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

// Initialize components when page loads
document.addEventListener("DOMContentLoaded", function () {
  // Initialize theme
  initTheme();

  // Initialize tooltips
  initTooltips();

  // Set up character counter
  const textarea = document.getElementById("email");
  if (textarea) {
    textarea.addEventListener("input", updateCharCount);
    updateCharCount(); // Initial count
  }

  // Set up form submission with loading indicator
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", showLoading);
  }

  // Set up progress steps - make step 1 active by default
  highlightCurrentStep(1);

  // Add event listeners to all theme toggle buttons
  const themeToggleButtons = document.querySelectorAll(
    "#theme-toggle, .theme-toggle"
  );
  themeToggleButtons.forEach((button) => {
    if (button) {
      button.addEventListener("click", toggleTheme);
    }
  });
});

// Progress steps highlighting
function highlightCurrentStep(step) {
  document.querySelectorAll(".progress-step").forEach((el, index) => {
    if (index + 1 <= step) {
      el.classList.add("active");
    } else {
      el.classList.remove("active");
    }
  });
}

// Function to copy results to clipboard (correctly named to match the onclick handler)
function copyResultsToClipboard() {
  const emailText = document.querySelector(".email-text").textContent;
  const spamConfidence =
    document.getElementById("spamConfidenceText").textContent;
  const notSpamConfidence = document.getElementById(
    "notSpamConfidenceText"
  ).textContent;
  const prediction = document.querySelector(".spam-indicator h3").textContent;
  const result = `Prediction: ${prediction}\nSpam Likelihood: ${spamConfidence}\nLegitimate Email Likelihood: ${notSpamConfidence}\nAnalyzed Text: ${emailText}`;

  navigator.clipboard
    .writeText(result)
    .then(() => {
      showToast("Results copied to clipboard!");
    })
    .catch(() => {
      showToast("Failed to copy results.", "danger");
    });
}

// Function to show toast notifications
function showToast(message, type = "primary") {
  const toastElement = document.getElementById("toastMessage");
  const toastBody = toastElement.querySelector(".toast-body");

  // Update toast message and type
  toastBody.textContent = message;
  toastElement.className = `toast align-items-center text-bg-${type} border-0`;

  // Show toast
  const toast = new bootstrap.Toast(toastElement);
  toast.show();
}
