function fetchCountries(selectId) {
  fetch('https://restcountries.com/v3.1/all?fields=name')
      .then(response => response.json())
      .then(data => {
          const select = document.getElementById(selectId);
          // select.innerHTML = '<option value="">Choose...</option>';
          data.sort((a, b) => a.name.common.localeCompare(b.name.common));
          data.forEach(country => {
              const option = document.createElement('option');
              option.value = country.name.common;
              option.text = country.name.common;
              select.appendChild(option);
          });
      })
      .catch(error => console.error('Error fetching countries:', error));
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// mainhub/adminhub/static/adminhub/registration.js

function validateInput(input) {
  const feedbackElementId = input.id + '_feedback';
  const feedbackElement = document.getElementById(feedbackElementId);
  let regex;
  let isValid = true;
  let message = '';

  if (input.value.trim() === '') {
    feedbackElement.textContent = '';
    feedbackElement.className = ''; 
    return;
}

  switch (input.id) {
      case 'full_name':
      case 'guardian_full_name':
          regex = /^[a-zA-Z\s/.-]+$/; 
          message = 'Full name must contain only letters, spaces, slashes (/), hyphens (-), and periods (.).';
          break;
      case 'nickname':
          regex = /^[a-zA-Z\s/.-]*$/; 
          message = 'Nickname must contain only letters, spaces, slashes (/), hyphens (-), and periods (.).';
          break;
      case 'ic_number':
      case 'guardian_ic_number':
          const selId  = (input.id === 'ic_number') ? 'student_id_type'
                                              : 'guardian_id_type';
          const idType = document.getElementById(selId)?.value || 'mykad';
          if (idType === 'mykad') {            // Malaysian NRIC / MyKid
              regex   = /^\d{12}$/;
              message = 'IC number must be exactly 12 digits.';
          } else if (idType === 'passport') {  // Passport (any country)
              regex   = /^[A-Za-z0-9]{6,20}$/;
              message = 'Passport number must be 6–20 letters or digits.';
          } else {                             // Birth certificate
              regex   = /^\d{6,15}$/;
              message = 'Birth-certificate number must be 6–15 digits.';
          }
          break;
      case 'guardian_contact_number':
          regex = /^0(1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-9])[0-9]{7,8}$/; 
          message = 'Please enter a valid Malaysian phone number format.';
          break;
      case 'postal_code':
          regex = /^\d{5}$/; 
          message = 'Postal code must be exactly 5 digits.';
          break;
      case 'email':
          regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/; 
          message = 'Please enter a valid email address in the format: alias@example.com.';
          break;
      default:
          break;
  }

  if (!regex.test(input.value)) {
      feedbackElement.textContent = message;
      feedbackElement.classList.add('error', 'lh-1');
      isValid = false;
  } else {
    feedbackElement.textContent = ''; 
    feedbackElement.classList.remove('error', 'lh-1')
    isValid = true;
  }

  return isValid;
}

document.addEventListener("DOMContentLoaded", function() {
  const studentIdSelect  = document.getElementById('student_id_type');
  const guardianIdSelect = document.getElementById('guardian_id_type');

  if (studentIdSelect) {
    studentIdSelect.addEventListener('change', () =>
      validateInput(document.getElementById('ic_number'))
    );
  }
  if (guardianIdSelect) {
    guardianIdSelect.addEventListener('change', () =>
      validateInput(document.getElementById('guardian_ic_number'))
    );
  }

  const nextButton = document.querySelector(".btn-next");
  const prevButton = document.querySelector(".btn-prev");
  let currentSection = 1
  
  function showSection(sectionNumber) {
    // Update section content visibility
    document.querySelectorAll(".section-content").forEach((section) => {
      section.classList.remove("active");
    });
    document.querySelector(`[data-section="${sectionNumber}"]`).classList.add("active");
    

    /**
     * Update step icons
     */
    document.querySelectorAll(".step").forEach((step, index) => {
      const iconDiv = step.querySelector(".mb-2 > div");
      if (index < sectionNumber) {
        iconDiv.classList.remove("bg-white", "border", "border-1", "border-success-subtle", "rounded-circle", "text-success", "text-opacity-50", "d-flex", "align-items-center", "justify-content-center");
        iconDiv.classList.add("bg-success", "rounded-circle", "text-white", "d-flex", "align-items-center", "justify-content-center");
      } else {
        iconDiv.classList.remove("bg-success", "rounded-circle", "text-white", "d-flex", "align-items-center", "justify-content-center");
        iconDiv.classList.add("bg-white", "border", "border-1", "border-success-subtle", "rounded-circle", "text-success", "text-opacity-50", "d-flex", "align-items-center", "justify-content-center");
      }
    });

    /**
     * Update progress bars
     */
    document.querySelectorAll(".progress-bar").forEach((bar, index) => {
      if (index < sectionNumber - 1) {
        bar.style.width = "100%";
      } else {
        bar.style.width = "0%";
      }
    });
    
    if (sectionNumber === 4) {
      nextButton.textContent = "Submit";
    } else {
      nextButton.textContent = "Next";
    }

    prevButton.style.display = sectionNumber === 1 ? "none" : "inline-block";
  }

  /**
   * for validation fields and 
   */
  const validationToast = new bootstrap.Toast(document.getElementById('validationToast'), {
    autohide: true,
    delay: 15000  // Increased to 5 seconds to give more time to read
  });

  nextButton.addEventListener("click", function(event) {

    const currentSectionContent = document.querySelector(`.section-content[data-section="${currentSection}"]`);
    const requiredFields = currentSectionContent.querySelectorAll('input[required], select[required], textarea[required]');
    const fileInput = document.getElementById('file-input');
    const agreementsCheck = document.getElementById('agreements_check');

    let isValid = true;
    let emptyFields = [];
    let customMessage = "";

    requiredFields.forEach(field => {
      if (!field.value.trim()) {
        isValid = false;
        field.classList.add('is-invalid');
        let fieldName = field.getAttribute('placeholder') || 
                      currentSectionContent.querySelector(`label[for="${field.id}"]`)?.textContent ||
                      field.name;
      emptyFields.push(fieldName);
      } else {
        field.classList.remove('is-invalid');
      }
    });

    if (currentSection === 4) {
      if (!fileInput.value) {
        isValid = false;
        customMessage = "Please upload a receipt before proceeding."; // Custom message for file input
        fileInput.classList.add('is-invalid');
      } else {
        fileInput.classList.remove('is-invalid'); // Remove invalid class if valid
      }
  
      if (!agreementsCheck.checked) {
        isValid = false;
        customMessage = "You must agree to the Privacy Statement and Terms and Conditions."; // Custom message for checkbox
        agreementsCheck.classList.add('is-invalid');
      } else {
        agreementsCheck.classList.remove('is-invalid'); // Remove invalid class if valid
      }
    }

    const validationRequiredFields = currentSectionContent.querySelectorAll('#full_name, #guardian_full_name, #nickname, #ic_number, #guardian_ic_number, #guardian_contact_number, #postal_code, #email')
    const allInputsValid = Array.from(validationRequiredFields).every(field => validateInput(field));

    if (isValid && allInputsValid) {
      if (currentSection < 4) {
        event.preventDefault();

        currentSection++;
        showSection(currentSection);
  
        nextButton.textContent = currentSection === 4 ? "Submit" : "Next";
  
        console.log(currentSection);
      } else if (currentSection === 4) {

        fetch('{% url "reg" %}', {
          method: 'POST',
          body: new FormData(this),
          headers: {
              'X-CSRFToken': getCookie('csrftoken')
          }
        })

        
        console.log(currentSection);
        
        return true;
      }
      
    } else {
      event.preventDefault();
      const toastMessage = document.getElementById('toastMessage');

      if (emptyFields.length > 0) {
        customMessage = `Please fill in the following required fields: <strong>${emptyFields.join(', ')}</strong>`;
      } else if (!allInputsValid) {
        customMessage = 'Please ensure all inputs are valid before proceeding.'
      }
      toastMessage.innerHTML = customMessage;
      console.log("else")

      validationToast.show();
    }
    

  });

  prevButton.addEventListener("click", function() {
    if (currentSection > 1) {
      currentSection--;
      showSection(currentSection);
      document.querySelector(".btn-next").innerHTML = "Next";
      console.log(currentSection)
    }
  });

  showSection(currentSection);

  /**
   * for selection box
   */
  const customSelects = document.querySelectorAll('.custom-select select');
  
  customSelects.forEach(select => {
    select.addEventListener('focus', function() {
      this.size = 1;
    });

    select.addEventListener('blur', function() {
      this.size = 1;
    });

    select.addEventListener('change', function() {
      this.size = 1;
      this.blur();
    });
  });

  /**
   * for course selection section
   */
  const addCourseButton = document.getElementById("add-course");
  const coursesContainer = document.getElementById("courses-container");

  function toggleRemoveButtons() {
    const removeButtons = coursesContainer.querySelectorAll('.remove_button');  
    const shouldShow = coursesContainer.children.length > 1;
    removeButtons.forEach(button => button.style.display = shouldShow ? 'block' : 'none');
  }

  addCourseButton.addEventListener("click", function () {
    const newRow = coursesContainer.querySelector(".course-row").cloneNode(true);
    const inputs = newRow.querySelectorAll("select");
    inputs.forEach(input => {
      input.value = "";
      input.id = input.id + Date.now();
    });
    coursesContainer.appendChild(newRow);
    toggleRemoveButtons();
  });

  coursesContainer.addEventListener('click', function(e) {
    if (e.target.closest('.remove_button')) {
      e.target.closest('.course-row').remove();
      toggleRemoveButtons();
    }
  });
  
  toggleRemoveButtons();

  /**
   * For 'other' option 
   */
  let guardian_salutation_select = document.getElementById('guardian_salutation');
  let other_salutation_container = document.getElementById('other_salutation_container');
  // let other_salutation_container_placeholder = document.getElementById('other_salutation_container_placeholder');
  let other_salutation_input = document.getElementById('other_salutation')

  guardian_salutation_select.onchange = function() {
    if (guardian_salutation_select.value === 'other') {
      other_salutation_container.style.display = 'block'; 
      other_salutation_input.setAttribute("required", "required");
      // other_salutation_container_placeholder.style.display = 'none'; 
    } else {
      other_salutation_container.style.display = 'none'; 
      other_salutation_input.removeAttribute("required");
      other_salutation_input.value = "";
      // other_salutation_container_placeholder.style.display = 'block'; 
    }
  }
  
  let guardian_relationship_select = document.getElementById('guardian_relationship');
  let other_relationship_container = document.getElementById('other_relationship_container');
  let other_relationship_container_placeholder = document.getElementById('other_relationship_container_placeholder');
  let other_relationship_input = document.getElementById('other_relationship')


  guardian_relationship_select.onchange = function() {
    if (guardian_relationship_select.value === 'other') {
      other_relationship_container.style.display = 'block'; 
      other_relationship_input.setAttribute("required", "required");
      other_relationship_container_placeholder.style.display = 'none'; 
    } else {
      other_relationship_container.style.display = 'none'; 
      other_relationship_input.removeAttribute("required");
      other_relationship_input.value = "";
      other_relationship_container_placeholder.style.display = 'block'; 
    }
  }

  // const inviteForm = document.getElementById('inviteCodeForm');

  // inviteForm.addEventListener('submit', function(e) {
  //   e.preventDefault();
  //   document.getElementById('loadingScreen').style.display = 'block';

  //   console.log("test")
    
  //   fetch('{% url "invite_code_entry" %}', {
  //     method: 'POST',
  //     body: new FormData(this),
  //     headers: {
  //       'X-CSRFToken': getCookie("csrftoken")
  //     }
  //   })
  //   .then(response => response.json())
  //   .then(data => {
  //     document.getElementById('loadingScreen').style.display = 'none';

  //     console.log("test")

  //     if (data.status === 'success') {
  //       window.location.href = '{% url "reg" %}';
  //     } else {
  //       var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
  //       errorModal.show();
  //     }
  //   })
  //   .catch(error => {
  //     console.error('Error:', error);
  //     document.getElementById('loadingScreen').style.display = 'none';
  //   });
  // });
});