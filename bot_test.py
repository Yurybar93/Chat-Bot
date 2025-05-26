import requests

BOT_TOKEN = "7398033193:AAE9iO70cjTBXVRhz9tcOAt7UWmEN4PZJQ4"  # Замените на ваш токен
response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe")
print(response.json())