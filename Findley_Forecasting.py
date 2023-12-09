#!/usr/local/bin/python3

"""
* Name : Findley_Forecasting.py 
* Author: David Findley
* Created : 05/04/2023 - Finalized
* Course: CIS 152 - Data Structures
* Version: 1.0
* OS: macOS 13.2.1
* IDE: Visual Studio Code
* Copyright : This is my own original work 
* based on specifications issued by our instructor
* Academic Honesty: I attest that this is my original work.
* I have not used unauthorized source code, either modified or
* unmodified. I have not given other fellow student(s) access
* to my program.
"""

import sys
import requests
from PyQt5 import QtWidgets, QtGui, QtCore

class WeatherApp(QtWidgets.QMainWindow):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.weather_data = {} # stores the weather data for each city
        self.hash_table = {} # stores the weather data for each city in a hash table
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(200, 200, 500, 400)

        # Create widgets
        self.city_label = QtWidgets.QLabel("City:")
        self.city_input = QtWidgets.QLineEdit()
        self.search_button = QtWidgets.QPushButton("Search")
        self.weather_table = QtWidgets.QTableWidget()
        self.weather_table.setColumnCount(4)
        self.weather_table.setHorizontalHeaderLabels(["City", "Temperature", "Humidity", "Condition"])

        # Create layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.weather_table)

        # Set main layout
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect signals to slots
        self.search_button.clicked.connect(self.search_weather)

        self.show()

    def search_weather(self):
        city = self.city_input.text()

        if not city:
            return

        # If the weather data for the city is already in the hash table, get it from there
        if city in self.hash_table:
            weather = self.hash_table[city]
        # Otherwise, get the weather data from the API and add it to the hash table
        else:
            weather = self.get_weather(city)
            self.hash_table[city] = weather

        if weather:
            self.display_weather(weather)
        else:
            self.display_error("City not found.")

    def get_weather(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=imperial"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            # Extract the relevant weather data from the API response
            name = data["name"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"]
            return {"name": name, "temperature": temperature, "humidity": humidity, "condition": condition}
        else:
            return None

    def display_weather(self, weather):
        # Clear the weather table
        self.weather_table.setRowCount(0)

        # Insert a new row in the weather table and add the weather data to it
        row_count = self.weather_table.rowCount()
        self.weather_table.insertRow(row_count)
        self.weather_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(weather["name"]))
        self.weather_table.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(weather["temperature"])))
        self.weather_table.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(weather["humidity"])))
        self.weather_table.setItem(row_count, 3, QtWidgets.QTableWidgetItem(weather["condition"]))

    def display_error(self, error_message):
        # Show an error message box with the given error message
        QtWidgets.QMessageBox.critical(self, "Error", error_message)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    api_key = "bd522d65c0d4b7e21fdfbd5df2bb2fa1"
    weather_app = WeatherApp(api_key)
    sys.exit(app.exec_())
