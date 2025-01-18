let weather = {
    apiKey: "6d055e39ee237af35ca066f35474e9df",
    fetchWeather: function (lat, lon) {
        fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${this.apiKey}`)
            .then((response) => {
                if (!response.ok) {
                    alert("Error fetching weather data");
                    throw new Error("Error fetching weather data");
                }
                return response.json();
            })
            .then((data) => this.displayWeather(data));
    },
    displayWeather: function (data) {
        const { name } = data;
        const { icon, description } = data.weather[0];
        const { temp, humidity } = data.main;
        const { speed } = data.wind;
        document.querySelector(".city").innerText = "Weather in " + name;
        document.querySelector(".icon").src =
            "https://openweathermap.org/img/wn/" + icon + ".png";
        document.querySelector(".description").innerText = description;
        document.querySelector(".temp").innerText = temp + "°C";
        document.querySelector(".humidity").innerText =
            "Humidity: " + humidity + "%";
        document.querySelector(".wind").innerText =
            "Wind speed: " + speed + " km/h";
        document.querySelector(".weather").classList.remove("loading");
        document.body.style.backgroundImage =
            "url('https://source.unsplash.com/1600x900/?" + name + "')";
    },
    getLocation: function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                // Success callback
                (position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    this.fetchWeather(lat, lon);
                },
                // Error callback
                (error) => {
                    console.error("Error getting location:", error);
                    alert("Unable to retrieve your location. Using default location.");
                    this.fetchWeather(51.5074, -0.1278); // Default coordinates (London)
                }
            );
        } else {
            alert("Geolocation is not supported by this browser");
            this.fetchWeather(51.5074, -0.1278); // Default coordinates (London)
        }
    }
};

// Initialize weather on page load
document.addEventListener('DOMContentLoaded', () => {
    weather.getLocation();
});
