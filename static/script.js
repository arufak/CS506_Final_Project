document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded and parsed");

    // Hourly Weather Slider
    const weatherIcon = document.querySelector('.weather-icon');
    const weatherDescription = document.getElementById('weather-description');
    // const temperatureSlider = document.getElementById('temperature-slider');
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
            // temperatureSlider.value = main.temp;
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

    const backgroundImage = images[weatherCondition] || images.default;
    weatherBackground.style.backgroundImage = `url(${backgroundImage})`;
}

    // // Temperature Slider
    // const tempSlider = document.querySelector('.temperature-slider input');
    // const tempValue = document.querySelector('.temperature-value');
    // if (tempSlider && tempValue) {
    //     tempSlider.addEventListener('input', () => {
    //         tempValue.textContent = `${tempSlider.value}°F`;
    //     });
    // }

    // recommended movies
    fetch('/recommended-movies')
    .then(response => response.json())
    .then(data => {
        const genresContainer = document.getElementById('recommended-genres');
        const suggestedMoviesContainer = document.getElementById('suggested-movies-content');

        // Display genres and movies by genre
        data.genres.forEach(genre => {
            const genreSection = document.createElement('div');
            genreSection.classList.add('movie-row');
            genreSection.innerHTML = `
                <h2>${genre}</h2>
                <button class="arrow-btn arrow-left">&lt;</button>
                <div class="movie-row-content" id="${genre}-content"></div>
                <button class="arrow-btn arrow-right">&gt;</button>
            `;
            genresContainer.appendChild(genreSection);

            const genreMoviesContainer = document.getElementById(`${genre}-content`);
            data.movies_by_genre[genre].forEach(movie => {
                const movieCard = document.createElement('div');
                movieCard.classList.add('movie-card');
                movieCard.dataset.title = movie.title;
                movieCard.dataset.description = movie.overview;
                movieCard.dataset.poster = movie.poster;
                movieCard.innerHTML = `
                    <img src="${movie.poster}" alt="${movie.title}">
                    <div class="movie-title">${movie.title}</div>
                `;
                genreMoviesContainer.appendChild(movieCard);

                movieCard.addEventListener('click', () => {
                    openModal(movie.title, movie.overview, movie.poster);
                });
            });

            // Add scrolling functionality
            const leftArrow = genreSection.querySelector('.arrow-left');
            const rightArrow = genreSection.querySelector('.arrow-right');
            let currentOffset = 0;
            const visibleMovieCount = 5;
            const totalMovies = Math.min(30, genreMoviesContainer.children.length);

            const updateMovieDisplay = () => {
                Array.from(genreMoviesContainer.children).forEach((movie, index) => {
                    if (index >= currentOffset && index < currentOffset + visibleMovieCount) {
                        movie.style.display = 'block';
                    } else {
                        movie.style.display = 'none';
                    }
                });

                leftArrow.disabled = currentOffset === 0;
                rightArrow.disabled = currentOffset + visibleMovieCount >= totalMovies;
            };

            rightArrow.addEventListener('click', () => {
                if (currentOffset + visibleMovieCount < totalMovies) {
                    currentOffset += visibleMovieCount;
                    updateMovieDisplay();
                }
            });

            leftArrow.addEventListener('click', () => {
                if (currentOffset > 0) {
                    currentOffset -= visibleMovieCount;
                    updateMovieDisplay();
                }
            });

            updateMovieDisplay();
        });

        // Display suggested movies
        const suggestedSection = document.createElement('div');
        suggestedSection.classList.add('movie-row');
        suggestedSection.innerHTML = `
            <h2>Suggested Movies</h2>
            <button class="arrow-btn arrow-left">&lt;</button>
            <div class="movie-row-content" id="suggested-content"></div>
            <button class="arrow-btn arrow-right">&gt;</button>
        `;
        suggestedMoviesContainer.appendChild(suggestedSection);

        const suggestedMoviesContent = document.getElementById('suggested-content');
        data.suggested_movies.forEach(movie => {
            const movieCard = document.createElement('div');
            movieCard.classList.add('movie-card');
            movieCard.dataset.title = movie.title;
            movieCard.dataset.description = movie.overview;
            movieCard.dataset.poster = movie.poster;
            movieCard.innerHTML = `
                <img src="${movie.poster}" alt="${movie.title}">
                <div class="movie-title">${movie.title}</div>
            `;
            suggestedMoviesContent.appendChild(movieCard);

            movieCard.addEventListener('click', () => {
                openModal(movie.title, movie.overview, movie.poster);
            });
        });

        // Add scrolling functionality for suggested movies
        const leftArrowSuggested = suggestedSection.querySelector('.arrow-left');
        const rightArrowSuggested = suggestedSection.querySelector('.arrow-right');
        let currentOffsetSuggested = 0;
        const visibleMovieCountSuggested = 5;
        const totalSuggestedMovies = Math.min(30, suggestedMoviesContent.children.length);

        const updateSuggestedMovieDisplay = () => {
            Array.from(suggestedMoviesContent.children).forEach((movie, index) => {
                if (index >= currentOffsetSuggested && index < currentOffsetSuggested + visibleMovieCountSuggested) {
                    movie.style.display = 'block';
                } else {
                    movie.style.display = 'none';
                }
            });

            leftArrowSuggested.disabled = currentOffsetSuggested === 0;
            rightArrowSuggested.disabled = currentOffsetSuggested + visibleMovieCountSuggested >= totalSuggestedMovies;
        };

        rightArrowSuggested.addEventListener('click', () => {
            if (currentOffsetSuggested + visibleMovieCountSuggested < totalSuggestedMovies) {
                currentOffsetSuggested += visibleMovieCountSuggested;
                updateSuggestedMovieDisplay();
            }
        });

        leftArrowSuggested.addEventListener('click', () => {
            if (currentOffsetSuggested > 0) {
                currentOffsetSuggested -= visibleMovieCountSuggested;
                updateSuggestedMovieDisplay();
            }
        });

        updateSuggestedMovieDisplay();
    })
    .catch(error => console.error('Error fetching recommended movies:', error));

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

        // Fetch additional movie details
        fetch(`/movie-details?title=${encodeURIComponent(title)}`)
            .then(response => response.json())
            .then(details => {
                const { release_year, tagline, genres, actors, director } = details;
                const genresList = genres.join(", ");
                const actorsList = actors.map(actor => actor.name).join(", ");
                const directorName = director ? director.name : "N/A";

                movieInfo.innerHTML = `
                    <h2>${title}</h2>
                    ${tagline ? `<p><em>—— ${tagline}</em></p>` : ''}
                    <p>${description}</p>
                    <p><strong>Release Year:</strong> ${release_year || 'N/A'}</p>
                    <p><strong>Genres:</strong> ${genresList || 'N/A'}</p>
                    <p><strong>Cast:</strong> ${actorsList || 'N/A'}</p>
                    <p><strong>Director:</strong> ${directorName}</p>
                `;
                modal.classList.remove("hidden");
            })
            .catch(error => console.error('Error fetching movie details:', error));
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

    // View Data Visualizations
    const viewDataBtn = document.getElementById('view-data-btn');
    const viewDataBtn2 = document.getElementById('view-data-btn-2');
    const closeDataBtn = document.getElementById('close-data-btn');
    const additionalContent = document.getElementById('additional-content');
    const dynamicContent = document.getElementById('dynamic-content');

    const loadContent = (url) => {
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                dynamicContent.innerHTML = data;
                additionalContent.classList.remove('hidden');
                viewDataBtn.classList.add('hidden');
                viewDataBtn2.classList.add('hidden');

                // Execute any scripts in the loaded HTML
                const scripts = dynamicContent.querySelectorAll('script');
                scripts.forEach(script => {
                    const newScript = document.createElement('script');
                    newScript.textContent = script.textContent;
                    document.body.appendChild(newScript);
                    document.body.removeChild(newScript);
                });
            })
            .catch(error => console.error('Error loading HTML content:', error));
    };

    viewDataBtn.addEventListener('click', () => {
        loadContent('/load-html/predicted_sunburst_chart.html');
    });

    viewDataBtn2.addEventListener('click', () => {
        loadContent('/load-html/predicted_interactive_genre_popularity_radar_chart.html');
    });

    closeDataBtn.addEventListener('click', () => {
        additionalContent.classList.add('hidden');
        viewDataBtn.classList.remove('hidden');
        viewDataBtn2.classList.remove('hidden');
        dynamicContent.innerHTML = ''; // Clear the content when closing
    });
});
