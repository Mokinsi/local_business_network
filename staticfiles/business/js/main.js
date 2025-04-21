document.addEventListener("DOMContentLoaded", () => {
    // Select form elements
    const form = document.querySelector("form");
    const locationInput = document.querySelector("#location");
    const serviceInput = document.querySelector("#service");
    const businessList = document.querySelector(".business-list");
    const loadingIndicator = document.querySelector(".loading-indicator");

    // Dark mode toggle
    document.getElementById('dark-mode-toggle').addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        businessList.classList.toggle('dark-mode', document.body.classList.contains('dark-mode'));
    });

    // Form validation
    form.addEventListener("submit", (event) => {
        let hasError = false;

        // Validate location
        if (locationInput.value.length < 3) {
            alert("Location must be at least 3 characters long.");
            hasError = true;
        }

        // Validate service
        if (serviceInput.value.length < 3) {
            alert("Service must be at least 3 characters long.");
            hasError = true;
        }

        if (hasError) {
            event.preventDefault(); // Stop form submission if validation fails
        }
    });

    // Real-time search functionality with debounce
    let debounceTimeout;

    const debounceFetchBusinesses = () => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(fetchBusinesses, 300); // Delay of 300ms
    };

    locationInput.addEventListener("input", debounceFetchBusinesses);
    serviceInput.addEventListener("input", debounceFetchBusinesses);

    const fetchBusinesses = async () => {
        const location = locationInput.value.trim();
        const service = serviceInput.value.trim();

        // Skip fetching if both fields are empty
        if (!location && !service) {
            businessList.innerHTML = "<p style='text-align: center;'>Please enter a location or service to search.</p>";
            return;
        }

        // Show loading indicator
        loadingIndicator.style.display = "block";

        try {
            // Send a GET request to the search endpoint
            const response = await fetch(`/business/search?location=${encodeURIComponent(location)}&service=${encodeURIComponent(service)}`);
            if (!response.ok) throw new Error("Failed to fetch businesses.");

            const businesses = await response.json();

            // Update the business list
            businessList.innerHTML = ""; // Clear current list
            if (businesses.length === 0) {
                businessList.innerHTML = "<p style='text-align: center;'>No businesses found for the specified criteria.</p>";
                return;
            }

            // Dynamically create business cards
            businesses.forEach((business) => {
                const card = document.createElement("div");
                card.classList.add("business-card");
                card.innerHTML = `
                    ${business.overview_picture ? `<img src="${business.overview_picture}" alt="${business.business_name}">` : ""}
                    <h3>${business.business_name}</h3>
                    <p><strong>Services Offered:</strong> ${business.services_offered}</p>
                    <p><strong>Location:</strong> ${business.location}</p>
                    <p><strong>Contact:</strong> ${business.contact_phone}</p>
                    <p><strong>Average Rating:</strong> ${business.avg_rating || "No ratings yet."}</p>
                    <a href="/business/view_business_profile/${business.id}">View Profile</a>
                `;
                businessList.appendChild(card);
            });
        } catch (error) {
            console.error("Error fetching businesses:", error);
            businessList.innerHTML = "<p style='text-align: center;'>An error occurred while fetching businesses. Please try again later.</p>";
        } finally {
            loadingIndicator.style.display = "none"; // Hide loading
        }
    };
});
