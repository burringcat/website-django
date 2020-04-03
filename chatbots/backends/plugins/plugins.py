import json
import requests
from django.conf import settings
class ChatBotPlugin:
    cmd = None
    args = 0
    is_enabled = True
    @classmethod
    def get_message(cls, *args):
        return ""

class WeatherPlugin(ChatBotPlugin):
    cmd = "weather"
    args = 1
    test_json = '{"coord":{"lon":-0.13,"lat":51.51},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],"base":"stations","main":{"temp":283.48,"feels_like":280.79,"temp_min":281.48,"temp_max":285.37,"pressure":1019,"humidity":57},"visibility":10000,"wind":{"speed":1.5,"deg":230},"clouds":{"all":98},"dt":1585940624,"sys":{"type":1,"id":1412,"country":"GB","sunrise":1585891820,"sunset":1585939000},"timezone":3600,"id":2643743,"name":"London","cod":200}'
    @classmethod
    def data_to_readable_str(cls, data:dict) -> str:
        if data.get('cod') != 200:
            return "request to openweathermap not successful"
        celsius = lambda k: format(k - 273.15, '.3f')
        return f"{data['name']} {data['sys']['country']}: {data['weather'][0]['description']} {celsius(data['main']['temp'])} °C"
    @classmethod
    def get_message(cls, *args):
        if not settings.CHATBOTS_OPENWEATHERMAP_API_KEY:
            return "empty openweathermap api key"
        if len(args) < 1 or not args[0]:
            return "invalid city name"
        city = " ".join(args)
        request_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.CHATBOTS_OPENWEATHERMAP_API_KEY}'
        data_json = WeatherPlugin.test_json if settings.DEBUG else requests.get(request_url).text
        try:
            data = json.loads(data_json)
        except:
            return f"can't load weather json data. city: {city}"
        return cls.data_to_readable_str(data)


