document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded and parsed");

    // Hourly Weather Slider
    const weatherIcon = document.querySelector('.weather-icon');
    const weatherDescription = document.getElementById('weather-description');
    const temperatureSlider = document.getElementById('temperature-slider');
    const temperatureValue = document.getElementById('temperature-value');
    const feelsLikeValue = document.getElementById('feels-like-value');
    const hourlyContainer = document.getElementById('hourly-container');
    const arrowLeft = document.getElementById('arrow-left');
    const arrowRight = document.getElementById('arrow-right');
    const weatherBackground = document.getElementById('weather-background');

    fetch('/weather')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }

            const weather = data.weather[0];
            const main = data.main;

            const simplifiedDescription = simplifyWeatherDescription(weather.description);
            weatherIcon.textContent = getWeatherIcon(weather.icon);
            weatherDescription.textContent = `The weather is ${simplifiedDescription} in Boston, MA`;
            temperatureSlider.value = main.temp;
            temperatureValue.textContent = `${main.temp.toFixed(2)}°F`;
            feelsLikeValue.textContent = `${main.feels_like.toFixed(2)}°F`;

            updateBackground(weather.icon, simplifiedDescription);

            fetch('/hourly-weather')
                .then(response => response.json())
                .then(hourlyData => {
                    if (hourlyData.error) {
                        console.error(hourlyData.error);
                        return;
                    }

                    const hourlyWeather = getHourlyWeatherData(hourlyData);

                    let currentOffset = 0;

                    const updateHourlyWeather = () => {
                        const dataToShow = hourlyWeather.slice(currentOffset, currentOffset + 3);
                        hourlyContainer.innerHTML = dataToShow.map(d => 
                            `<div class="hourly-item">${d.time} ${d.weather} ${d.temp}°F</div>`
                        ).join('');
                        arrowLeft.disabled = currentOffset === 0;
                        arrowRight.disabled = currentOffset + 3 >= hourlyWeather.length;
                    };

                    arrowRight.addEventListener('click', () => {
                        if (currentOffset + 3 < hourlyWeather.length) currentOffset++;
                        updateHourlyWeather();
                    });

                    arrowLeft.addEventListener('click', () => {
                        if (currentOffset > 0) currentOffset--;
                        updateHourlyWeather();
                    });

                    updateHourlyWeather();
                })
                .catch(error => console.error('Error fetching hourly weather data:', error));
        })
        .catch(error => console.error('Error fetching weather data:', error));


function getWeatherIcon(iconCode) {
    const iconMap = {
        '01d': '☀️', '01n': '🌙',
        '02d': '🌤️', '02n': '🌤️',
        '03d': '☁️', '03n': '☁️',
        '04d': '☁️', '04n': '☁️',
        '09d': '🌧️', '09n': '🌧️',
        '10d': '🌦️', '10n': '🌦️',
        '11d': '⛈️', '11n': '⛈️',
        '13d': '❄️', '13n': '❄️',
        '50d': '🌫️', '50n': '🌫️'
    };
    return iconMap[iconCode] || '❓';
}

function simplifyWeatherDescription(description) {
    const descriptionMap = {
        "clear sky": "clear",
        "few clouds": "partly cloudy",
        "scattered clouds": "cloudy",
        "broken clouds": "cloudy",
        "shower rain": "rainy",
        "rain": "rainy",
        "thunderstorm": "stormy",
        "snow": "snowy",
        "mist": "foggy",
        "light rain": "slightly rainy"
    };
    return descriptionMap[description.toLowerCase()] || description;
}

function getHourlyWeatherData(data) {
    return data.list.slice(0, 8).map(item => {
        const date = new Date(item.dt * 1000);
        const hours = date.getHours();
        const time = hours > 12 ? `${hours - 12}PM` : `${hours}AM`;
        return {
            time: time,
            weather: getWeatherIcon(item.weather[0].icon),
            temp: item.main.temp.toFixed(2)
        };
    });
}

function updateBackground(iconCode, description) {
    const images = {
        clear: 'https://images.pexels.com/photos/789152/pexels-photo-789152.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        cloudy: 'https://images.pexels.com/photos/19670/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        rainy: 'https://images.pexels.com/photos/1154510/pexels-photo-1154510.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        stormy: 'https://images.pexels.com/photos/1102915/pexels-photo-1102915.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        snowy: 'https://images.pexels.com/photos/1853384/pexels-photo-1853384.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        foggy: 'https://images.pexels.com/photos/978844/pexels-photo-978844.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        default: 'https://images.pexels.com/photos/13695339/pexels-photo-13695339.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2'
    };

    const timeOfDay = iconCode.endsWith('d') ? 'Day' : 'Night';
    const weatherCondition = description.split(' ')[0]; // Get the first word of the description

    const backgroundImage = images[weatherCondition] || images.Default;
    weatherBackground.style.backgroundImage = `url(${backgroundImage})`;
}

    // Temperature Slider
    const tempSlider = document.querySelector('.temperature-slider input');
    const tempValue = document.querySelector('.temperature-value');
    if (tempSlider && tempValue) {
        tempSlider.addEventListener('input', () => {
            tempValue.textContent = `${tempSlider.value}°F`;
        });
    }

    // Movie Section Navigation
    const movieRows = document.querySelectorAll('.movie-row');
    movieRows.forEach(row => {
        const movieContainer = row.querySelector('.movie-row-content');
        const movieArrowLeft = row.querySelector('.arrow-left');
        const movieArrowRight = row.querySelector('.arrow-right');
        const genre = row.querySelector('h2').textContent.toLowerCase();

        if (movieContainer && movieArrowLeft && movieArrowRight && genre) {
            console.log(`Fetching movies for genre: ${genre}`);
            fetch(`/movies?genre=${genre}`)
                .then(response => response.json())
                .then(movieData => {
                    console.log(`Movies for genre ${genre}:`, movieData);
                    if (movieData.error) {
                        console.error(movieData.error);
                        return;
                    }

                    let currentOffset = 0;
                    const visibleMovieCount = 5;

                    const updateMovieDisplay = () => {
                        const moviesToShow = movieData.slice(currentOffset, currentOffset + visibleMovieCount);
                        movieContainer.innerHTML = moviesToShow.map(movie => `
                            <div class="movie-card" data-title="${movie.title}" data-description="${movie.overview}" data-poster="${movie.poster_path}">
                                <img src="${movie.poster_path}" alt="${movie.title}">
                                <div>${movie.title}</div>
                            </div>
                        `).join('');

                        movieArrowLeft.disabled = currentOffset === 0;
                        movieArrowRight.disabled = currentOffset + visibleMovieCount >= movieData.length;

                        const movieCards = movieContainer.querySelectorAll('.movie-card');
                        movieCards.forEach(card => {
                            card.addEventListener('click', () => {
                                const title = card.getAttribute('data-title');
                                const description = card.getAttribute('data-description');
                                const poster = card.getAttribute('data-poster');
                                console.log(`Opening modal for movie: ${title}`);
                                openModal(title, description, poster);
                            });
                        });
                    };

                    movieArrowRight.addEventListener('click', () => {
                        if (currentOffset + visibleMovieCount < movieData.length) {
                            currentOffset += visibleMovieCount;
                            updateMovieDisplay();
                        }
                    });

                    movieArrowLeft.addEventListener('click', () => {
                        if (currentOffset > 0) {
                            currentOffset -= visibleMovieCount;
                            updateMovieDisplay();
                        }
                    });

                    updateMovieDisplay();
                })
                .catch(error => console.error('Error fetching movies:', error));
        }
    });

    // Modal functionality
    const modal = document.getElementById("modal");
    const closeBtn = document.querySelector(".close-btn");

    function openModal(title, description, poster) {
        console.log(`Modal data: ${title}, ${description}, ${poster}`);
        const moviePoster = modal.querySelector("#modal-poster");
        const movieInfo = modal.querySelector(".movie-info");

        if (moviePoster && movieInfo) {
            moviePoster.src = poster;
            moviePoster.alt = title;
            movieInfo.innerHTML = `
                <h2>${title}</h2>
                <p>${description}</p>
            `;
            modal.classList.remove("hidden");
        } else {
            console.error('Modal elements not found:', {
                moviePoster,
                movieInfo
            });
        }
    }

    if (modal) {
        // Close modal on close button click or clicking outside the modal
        closeBtn?.addEventListener("click", () => {
            modal.classList.add("hidden");
        });
        modal.addEventListener("click", (e) => {
            if (e.target === modal) {
                modal.classList.add("hidden");
            }
        });
    }

    // Back to Top Button
    const backToTopButton = document.querySelector('.bring-to-top');
    if (backToTopButton) {
        backToTopButton.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});