
let currentStep = 1;

function showStep(step) {
    const sections = document.querySelectorAll('.form-section');
    const steps = document.querySelectorAll('.step');

    sections.forEach(section => section.classList.remove('active'));
    steps.forEach(stepElem => stepElem.classList.remove('active'));

    document.querySelector(`.form-section[data-section="${step}"]`).classList.add('active');
    document.querySelector(`.step[data-step="${step}"]`).classList.add('active');

    if (step === 1) {
        fetchCountries('student-country');
    } else if (step === 2) {
        fetchCountries('guardian-country');
    }

    document.getElementById('prevBtn').style.display = (step === 1) ? 'none' : 'inline';
    document.getElementById('nextBtn').innerText = (step === sections.length) ? 'Submit' : 'Next';
}

function nextPrev(n) {
    const sections = document.querySelectorAll('.form-section');
    if (n === 1 && !validateForm()) return false;

    currentStep += n;
    if (currentStep > sections.length) {
        document.querySelector('form').submit();
        return false;
    }
    showStep(currentStep);
}

function validateForm() {
    // Add form validation if needed
    return true;
}

function fetchCountries(selectId) {
    fetch('https://restcountries.com/v2/all')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById(selectId);
            select.innerHTML = '<option value="">Select Country</option>';
            data.forEach(country => {
                const option = document.createElement('option');
                option.value = country.name;
                option.text = country.name;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching countries:', error));
}

function copyAddress() {
    const studentAddress = document.getElementById('student-address').value;
    const studentCity = document.getElementById('student-city').value;
    const studentState = document.getElementById('student-state').value;
    const studentPostal = document.getElementById('student-postal').value;
    const studentCountry = document.getElementById('student-country').value;

    document.getElementById('guardian-address').value = studentAddress;
    document.getElementById('guardian-city').value = studentCity;
    document.getElementById('guardian-state').value = studentState;
    document.getElementById('guardian-postal-code').value = studentPostal;
    document.getElementById('guardian-country').value = studentCountry;
}

function handleFileUpload() {
    const fileInput = document.getElementById('file-upload-input');
    const fileInfo = document.getElementById('file-info');

    const file = fileInput.files[0];
    if (file) {
        const fileName = file.name;
        const fileExtension = fileName.split('.').pop();
        fileInfo.textContent = `File: ${fileName} (.${fileExtension})`;
    } else {
        fileInfo.textContent = '';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    showStep(currentStep);
    document.getElementById('prevBtn').style.display = 'none';
});

window.nextPrev = nextPrev;
window.copyAddress = copyAddress;
window.handleFileUpload = handleFileUpload;