// Email Spam Classifier interactive features


// Loading animation
function showLoading() {
  document.getElementById('loadingIndicator').style.display = 'block';
  document.querySelector('.submit-btn').disabled = true;
}

// Example emails
function fillExampleEmail(type) {
  let content = '';
  if (type === 'spam') {
    content = "CONGRATULATIONS! You've been selected to receive a FREE $1000 Walmart gift card! Click here to claim now: http://claim-your-gift.com Limited time offer, ACT NOW!";
  } else {
    content = "Dear Team,\n\nPlease find attached the meeting notes from yesterday's planning session. Let me know if you need any clarification.\n\nRegards,\nJohn";
  }
  document.getElementById('email').value = content;
  
  // Update character count if counter exists
  if (document.getElementById('charCounter')) {
    updateCharCount();
  }
}

// Character counter
function updateCharCount() {
  const textarea = document.getElementById('email');
  const charCounter = document.getElementById('charCounter');
  const count = textarea.value.length;
  
  charCounter.textContent = count + (count === 1 ? ' character' : ' characters');
  
  if (count > 200) {
    charCounter.style.color = '#dc3545';
  } else {
    charCounter.style.color = '#6c757d';
  }
}

// Toggle dark/light mode
function toggleTheme() {
  document.body.classList.toggle('dark-mode');
  const icon = document.getElementById('themeIcon');
  if (document.body.classList.contains('dark-mode')) {
    icon.classList.replace('bi-moon-fill', 'bi-sun-fill');
    localStorage.setItem('theme', 'dark');
  } else {
    icon.classList.replace('bi-sun-fill', 'bi-moon-fill');
    localStorage.setItem('theme', 'light');
  }
}

// Initialize theme from localStorage
function initTheme() {
  if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-mode');
    const icon = document.getElementById('themeIcon');
    if (icon) {
      icon.classList.replace('bi-moon-fill', 'bi-sun-fill');
    }
  }
}

// Initialize tooltips
function initTooltips() {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

// Initialize components when page loads
document.addEventListener('DOMContentLoaded', function() {
  // Initialize theme
  initTheme();
  
  // Initialize tooltips
  initTooltips();
  
  // Set up character counter
  const textarea = document.getElementById('email');
  if (textarea) {
    textarea.addEventListener('input', updateCharCount);
    updateCharCount(); // Initial count
  }
  
  // Set up form submission with loading indicator
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', showLoading);
  }
  
  // Set up progress steps - make step 1 active by default
  highlightCurrentStep(1);
});

// Progress steps highlighting
function highlightCurrentStep(step) {
  document.querySelectorAll('.progress-step').forEach((el, index) => {
    if (index + 1 <= step) {
      el.classList.add('active');
    } else {
      el.classList.remove('active');
    }
  });
}
                                                                                              
// Function to copy results to clipboard (correctly named to match the onclick handler)
function copyResultsToClipboard() {
  const emailText = document.querySelector('.email-text').textContent;
  const confidence = document.getElementById('confidenceText').textContent;
  const prediction = document.querySelector('.spam-indicator h3').textContent;
  const result = `Prediction: ${prediction}\nConfidence Level: ${confidence}%\nAnalyzed Text: ${emailText}`;

  navigator.clipboard.writeText(result).then(() => {
    showToast('Results copied to clipboard!');
  }).catch(() => {
    showToast('Failed to copy results.', 'danger');
  });
}

// Function to show toast notifications
function showToast(message, type = 'primary') {
  const toastElement = document.getElementById('toastMessage');
  const toastBody = toastElement.querySelector('.toast-body');

  // Update toast message and type
  toastBody.textContent = message;
  toastElement.className = `toast align-items-center text-bg-${type} border-0`;

  // Show toast
  const toast = new bootstrap.Toast(toastElement);
  toast.show();
}
