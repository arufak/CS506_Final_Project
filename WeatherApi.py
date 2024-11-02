import requests
import json
import pycountry

api_key = 'aef5b02291330e9c41692e83d46e6c73'




#This is for getting the location of the user and turning the country name inot the counrty ISO code for the openwaether api to use, let the user input zip code and country name"
country_name = "United States"
country = pycountry.countries.get(name=country_name)
country_code = country.alpha_2
zip_code = '02134'


url_location = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={api_key}'

response_location = requests.get(url_location)
if response_location.status_code == 200:
    data_location = response_location.json()
    latitude = data_location["lat"]
    longitude = data_location["lon"]
    print(json.dumps(data_location, indent=4))




#This is for getting the details of the weather based on location and time closes to now as the free version on openweather api only tracks weather every 3 hours
url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=imperial'

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    
    temperature = data["main"]["temp"]   
    feels_like = data["main"]["feels_like"]   
    description = data["weather"][0]["description"]
    main_weather = data["weather"][0]["main"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    visibility = data["visibility"] / 1000  

    icon_code = data["weather"][0]["icon"]
    part_of_day = "Day" if icon_code.endswith("d") else "Night"

    print(f"Temperature: {temperature:.2f}°F")
    print(f"Feels Like: {feels_like:.2f}°F")
    print(f"Weather: {main_weather} - {description}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print(f"Visibility: {visibility} km")
    print(f"Part of Day: {part_of_day}")
else:
    print('Error:', response.status_code)


