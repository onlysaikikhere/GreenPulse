/*let weather = {
    apiKey: "6d055e39ee237af35ca066f35474e9df", 
    fetchWeather: function (city) {
    fetch("https://api.openweathermap.org/data/2.5/weather?q=" +
        city +
        "&units=metric&appid=" +
        this.apiKey)
        .then((response) => {
        if (!response.ok) {
            alert("Invalid location");
            throw new Error("Invalid location");
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
    search: function () {
    this.fetchWeather(document.querySelector(".search-bar").value);
    },
};
let geocode = {
    reverseGeocode: function (latitude, longitude) {
    var apikey = "90a096f90b3e4715b6f2e536d934c5af";

    var api_url = "https://api.opencagedata.com/geocode/v1/json";

    var request_url =
        api_url +
        "?" +
        "key=" +
        apikey +
        "&q=" +
        encodeURIComponent(latitude + "," + longitude) +
        "&pretty=1" +
        "&no_annotations=1";

    var request = new XMLHttpRequest();
    request.open("GET", request_url, true);

    request.onload = function () {

        if (request.status == 200) {
        var data = JSON.parse(request.responseText);
        weather.fetchWeather(data.results[0].components.city);
        console.log(data.results[0].components.city)
        } else if (request.status <= 500) {

        console.log("unable to geocode! Response code: " + request.status);
        var data = JSON.parse(request.responseText);
        console.log("error msg: " + data.status.message);
        } else {
        console.log("server error");
        }
    };

    request.onerror = function () {
        console.log("unable to connect to server");
    };

    request.send(); 
    },
    getLocation: function() {
    function success (data) {
        geocode.reverseGeocode(data.coords.latitude, data.coords.longitude);
    }
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, console.error);
    }
    else {
        weather.fetchWeather("Manipal");
    }
    }
};

document.querySelector(".search button").addEventListener("click", function () {
    weather.search();
});

document
    .querySelector(".search-bar")
    .addEventListener("keyup", function (event) {
    if (event.key == "Enter") {
        weather.search();
    }
    });

weather.fetchWeather("Manipal");

document
    .querySelector(".search-bar")
    .addEventListener("keyup", function (event) {
    if (event.key == "Enter") {
        weather.search();
    }
    });

geocode.getLocation();*/
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