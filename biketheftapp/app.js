function goToMainPage() {
    document.getElementById("loginPage").style.display = "none";   // Hide login page
    document.getElementById("mainPage").style.display = "block";   // Show main page
    initMap();  // Initialize the map after login
}

function goBack() {
    document.getElementById("notificationsPage").style.display = "none";   // Hide notifications page
    document.getElementById("mainPage").style.display = "block";   // Show main page
}

document.getElementById("activateAlarmBtn").addEventListener("click", function () {
    const alarmAlert = document.getElementById("alarmAlert");
    alarmAlert.style.display = "block"; // Show the alert message
    setTimeout(function () {
        alarmAlert.style.display = "none"; // Hide the alert after a few seconds
    }, 4000); // Hide after 4 seconds
});

document.getElementById("notificationsBtn").addEventListener("click", function () {
    document.getElementById("mainPage").style.display = "none";  // Hide main page
    document.getElementById("notificationsPage").style.display = "block";  // Show notifications page
    displayNotifications(); // Display notifications when page is shown
});

const notifications = [
    "Theft detected near your bike!",
    "Lock activated successfully.",
    "Suspicious movement detected.",
    "Bike location updated.",
    "Camera feed started."
];

function displayNotifications() {
    const notificationsList = document.getElementById("notificationsList");
    notificationsList.innerHTML = ""; // Clear existing notifications
    notifications.forEach(notification => {
        const listItem = document.createElement("li");
        listItem.textContent = notification;
        notificationsList.appendChild(listItem);
    });
}

// Initialize Leaflet map
function initMap() {
    const mapElement = document.getElementById("map");
    const bikeLocation = [42.3601, -71.0589]; // Example coordinates

    const map = L.map(mapElement).setView(bikeLocation, 15);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    L.marker(bikeLocation).addTo(map).bindPopup("Bike Location").openPopup();
}


function showMainPage() {
    document.getElementById("loginPage").style.display = "none";  // Hide login page
    document.getElementById("mainPage").style.display = "block";  // Show theft detection page
    document.getElementById("notificationsPage").style.display = "none";  // Hide notifications page

    // Optionally, reset any dynamic content on the main page (like map, notifications)
    initMap(); // Re-initialize the map to reset the state
}

// Event listener for the Home button to always navigate to the Theft Detection page
document.getElementById("homeBtn").addEventListener("click", function() {
    goToMainPage();  // Function to show the main theft detection page
});

