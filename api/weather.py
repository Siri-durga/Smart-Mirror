import requests

def get_weather():
    """Fetch weather data from the API."""
    API_KEY = "865e56a715e6ea57f18edf64b6553780"
    CITY ="Kakinada"
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

    response = requests.get(URL)
    data = response.json()
    
    print("Weather API Response:", data)  # Debugging: Print full response

    if 'weather' in data and 'main' in data:
        return data['weather'][0]['description'], data['main']['temp']
    else:
        return None  # Handle error gracefully
