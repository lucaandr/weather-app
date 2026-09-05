import os
import sys
import requests
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

load_dotenv()


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
        QLabel, QPushButton{
            font-family: calibri;
        }
        QLabel#city_label{
            font-size: 40px;
            font-style: italic;
        }
        QLineEdit#city_input{
            font-size: 40px;
        }
        QPushButton#get_weather_button{
            font-size: 30px;
            font-weight: bold;
        }
        QLabel#temperature_label{
            font-size: 75px;
        }
        QLabel#emoji_label{
            font-size: 100px;
            font-family: Segoe UI emoji;
        }
        QLabel#description_label{
            font-size: 50px;
        }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = os.getenv("OPENWEATHER_API_KEY")

        if not api_key:
            self.display_errors("API key not found\nCheck your .env file")
            return

        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)

            response.raise_for_status()

            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_errors("Bad request\nPlease check your input")
                case 401:
                    self.display_errors("Unauthorized\nInvalid API key")
                case 403:
                    self.display_errors("Forbidden\nAccess is denied")
                case 404:
                    self.display_errors("Not found\nCity not found")
                case 500:
                    self.display_errors(
                        "Internal Server Error\nPlease try again later")
                case 502:
                    self.display_errors(
                        "Bad Gateway\nInvalid response from the server")
                case 503:
                    self.display_errors("Service Unavailable\nServer is down")
                case 504:
                    self.display_errors(
                        "Gateway Timeout\nNo response from the server")
                case _:
                    self.display_errors(f"HTTP error occurred: {http_error}")

        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")

    def display_errors(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        nume_easter_egg = data["name"].lower()
        if nume_easter_egg == "iulia":
            self.temperature_label.setStyleSheet(
                "font-size: 50px; color: #E91E63;")
            self.temperature_label.setText("Ubita!!!")
            self.emoji_label.setText("❤️❤️❤️")
            self.description_label.setStyleSheet(
                "font-size: 50px; color: #E91E63;")
            self.description_label.setText("Nu uita sa bei apa, pookie!")
            return

        self.temperature_label.setStyleSheet("font-size: 75px; color: black;")
        self.description_label.setStyleSheet("font-size: 50px; color: black;")

        temperatura_resimtita = data["main"]["feels_like"]
        id_temperatura_resimtita = data["weather"][0]["id"]
        print(temperatura_resimtita)
        self.temperature_label.setText(
            f"Feels like:{temperatura_resimtita:.0f}°C")
        cum_e_vremea = data["weather"][0]["description"]
        self.emoji_label.setText(
            self.get_weather_emoji(id_temperatura_resimtita))
        self.description_label.setText(cum_e_vremea)

    @staticmethod
    def get_weather_emoji(id_temperatura_resimtita):
        if 200 <= id_temperatura_resimtita <= 232:
            return "⛈️"
        elif 300 <= id_temperatura_resimtita <= 321:
            return "🌦️"
        elif 500 <= id_temperatura_resimtita <= 531:
            return "🌧️"
        elif 600 <= id_temperatura_resimtita <= 622:
            return "❄️"
        elif 701 <= id_temperatura_resimtita <= 781:
            return "🌫️"
        elif id_temperatura_resimtita == 800:
            return "☀️"
        elif 801 <= id_temperatura_resimtita <= 804:
            return "☁️"
        else:
            return "✨"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
