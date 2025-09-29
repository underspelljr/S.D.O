document.addEventListener('DOMContentLoaded', () => {
    // Initialize map centered on Oeiras, Portugal
    const oeirasCoords = [38.697, -9.302];
    const map = L.map('map').setView(oeirasCoords, 14);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let users = [];

    // Function to fetch users and populate dropdown
    async function fetchUsers() {
        try {
            const response = await fetch('/users');
            if (!response.ok) throw new Error('Failed to fetch users');
            users = await response.json();
        } catch (error) {
            console.error(error);
            alert('Could not load users. Please create a user first via the API at /docs.');
        }
    }

    // Function to fetch and display spots
    async function fetchAndDisplaySpots() {
        try {
            const response = await fetch('/spots');
            if (!response.ok) throw new Error('Failed to fetch spots');
            const spots = await response.json();
            spots.forEach(spot => addSpotMarker(spot));
        } catch (error) {
            console.error('Error fetching spots:', error);
        }
    }

    // Function to add a spot marker to the map
    function addSpotMarker(spot) {
        const marker = L.marker([spot.latitude, spot.longitude]).addTo(map);
        marker.bindPopup(`<b>${spot.name}</b><br>${spot.description || ''}<br><small>Added by: ${spot.created_by.name}</small>`);
    }

    // Handle map click event to create a new spot
    map.on('click', async (e) => {
        const { lat, lng } = e.latlng;
        
        if (users.length === 0) {
            alert('No users found. Please create a user first via the API docs (/docs) before adding a spot.');
            return;
        }

        const userOptions = users.map(user => `<option value="${user.id}">${user.name}</option>`).join('');

        const formHtml = `
            <div class="popup-form">
                <h3>Create New Spot</h3>
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
                <label for="description">Description:</label>
                <textarea id="description" name="description"></textarea>
                <label for="user">Created By:</label>
                <select id="user" name="user_id" required>
                    ${userOptions}
                </select>
                <button type="button" id="submitSpot">Create Spot</button>
            </div>
        `;

        const popup = L.popup()
            .setLatLng(e.latlng)
            .setContent(formHtml)
            .openOn(map);
        
        // Timeout to ensure the popup is in the DOM
        setTimeout(() => {
             document.getElementById('submitSpot').addEventListener('click', async () => {
                const name = document.getElementById('name').value;
                const description = document.getElementById('description').value;
                const userId = document.getElementById('user').value;

                if (!name || !userId) {
                    alert('Name and creator are required.');
                    return;
                }

                const newSpotData = {
                    name,
                    description,
                    latitude: lat,
                    longitude: lng,
                    user_id: parseInt(userId, 10),
                };

                try {
                    const response = await fetch('/spots', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(newSpotData),
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Failed to create spot');
                    }

                    const createdSpot = await response.json();
                    addSpotMarker(createdSpot);
                    map.closePopup();

                } catch (error) {
                    console.error('Error creating spot:', error);
                    alert(`Error: ${error.message}`);
                }
            });
        }, 100);
    });

    // Initial load
    async function initializeApp() {
        await fetchUsers();
        await fetchAndDisplaySpots();
    }

    initializeApp();
});