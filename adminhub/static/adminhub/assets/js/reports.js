// Call the function to set the current year
function selectYear(year) {
    const textbox = document.querySelector("details summary");
    textbox.innerHTML = year;
  
    // Send the selected year to the backend
    // Replace with actual backend endpoint later
    fetch("/backend-endpoint/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}",
      },
      body: JSON.stringify({ selected_year: year }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  
  function openSidebar() {
    const sidebar = document.querySelector(".sidebar");
    const body = document.body;
    sidebar.classList.toggle("hidden");
    body.classList.toggle("sidebar-open");
  }
  
  function toggleDropdown() {
    const dropdown = document.getElementById("user-menu-dropdown");
    dropdown.classList.toggle("hidden");
  }
  
  function dropdown() {
    document.querySelector("#submenu").classList.toggle("hidden");
    document.querySelector("#arrow").classList.toggle("rotate-180");
  }
  dropdown();
  
  document.addEventListener("DOMContentLoaded", function () {
    let currentMonth = new Date().getMonth(); // Get the current month (0-11)
    const monthNames = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];
  
    function getCurrentMonth() {
      document.getElementById("current-month").textContent =
        monthNames[currentMonth];
    }
    getCurrentMonth();
  
    function changeMonth(direction) {
      currentMonth += direction;
      if (currentMonth < 0) {
        currentMonth = 11;
      } else if (currentMonth > 11) {
        currentMonth = 0;
      }
      getCurrentMonth();
    }
  
    function closeDropDown(event) {
      const userDropdownContainer = document.getElementById(
        "user-menu-button-container"
      );
      const userDropdown = document.getElementById("user-menu-dropdown");
      if (!userDropdownContainer.contains(event.target)) {
        userDropdown.classList.add("hidden");
        console.log("closed");
      }
    }
  
    document.addEventListener("click", function (event) {
      closeDropDown(event);
    });
  
    window.changeMonth = changeMonth;
  });
  