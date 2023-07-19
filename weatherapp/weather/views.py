import requests
from django.shortcuts import render

def get_weather(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": location,
        "appid": api_key,
        "units": "imperial"  # Change to 'imperial' for Fahrenheit
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data.get("cod") == "404":
        city, *state = location.split(",")
        city = city.strip()
        state = "".join(state).strip()
        params["q"] = f"{city},{state}"
        response = requests.get(base_url, params=params)
        data = response.json()
        if data.get("cod") == "404":
            return {"error": "Location not found."}
    try:
        current_weather = {
            "location": data["city"]["name"] + ", " + data["city"]["country"],
            "temperature": data["list"][0]["main"]["temp"],
            "humidity": data["list"][0]["main"]["humidity"],
            "description": data["list"][0]["weather"][0]["description"],
            "latitude": data["city"]["coord"]["lat"],
            "longitude": data["city"]["coord"]["lon"]
        }
        forecast = []
        for item in data["list"][1:]:
            forecast.append({
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "description": item["weather"][0]["description"]
            })
        return {"current_weather": current_weather, "forecast": forecast}
    except KeyError:
        return {"error": "Weather data not available."}




def weather(request):
    if request.method == "POST":
        location = request.POST.get("location", "")
        api_key = "4054214bff185cc3196c087b076636eb"  # Replace with your actual API key
        weather_data = get_weather(api_key, location)
        return render(request, "weather.html", {"weather_data": weather_data})
    return render(request, "weather.html")
