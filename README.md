# Temperature and humidity sensor measurer

Project for the course Introduction to Applied IoT, Summer 2024

**Name:** Eldaras Zutautas <br>
**Student:** ez222eq

# Short project overview
For this project, I constructed a sensor node using a Raspberry Pi Pico W that reports temperature and humidity every hour to ThingSpeak, a free service that facilitates communication with internet-enabled devices.

**Approxiamtion of time needed for the project:**

Up to 2-3 hours total

# Objective
**Reasons for choosing the project:**
I chose this project because I've always felt that my room becomes very dry during the summer. I wanted to verify this, so I decided to create a sensor node to measure the actual humidity levels.

**Purposes of the project:**
The main objective of this project is twofold. Firstly, it aims to provide a learning experience about the Internet of Things (IoT), including understanding how to construct an IoT device and connect it to a platform for visualizing its data. Secondly, it seeks to manage and monitor the room's humidity and temperature.

**Insights gained by doing the project:**
The project offers an opportunity to gain an understanding of fundamental concepts in IoT and electrical circuits, providing valuable insights into these areas.

# Material
Component | Purpose    
-| -|
ESP8266 | A microcontroller used for data collection, data transfer, and data analysis. 
DHT11 | A sensor used for mesuring the humidity in the air asweel as the temperature 
5x Jumper wires | Wires for connecting the different components
Breadboard 800 points | A board used to easy connect the sensors without soldering 
Micro USB cable | Connection between Raspberry Pi Pico and a computer

I bought the Linnaeus Development kit for 399 SEK, so it had all of these components included.



# Computer setup
**Setting up the IDE:**

The first step was to decide which IDE to use. I chose Visual Studio Code. After installing it, I also installed the MicroPython extension to work with the Raspberry Pi Pico.

After that we need to configure the project for the Pico. That is why we use extension to do so.

![Alt text](images/ide_pic1.png)

After the configuration a ".micropico" config was created, therefore it means that the configuration was initialized correctly. From this point, we can try to connect the Raspberry Pi Pico to a computer and see, if our IDE detects it.

![Alt text](images/ide_pic2.png)

Note: it is mandatory to add a boot setup to Raspberry Pi Pico or else it will not work. Furthermore, the new updates for Pico would not detect the Pico, therefore had to use older versions.

In this project, I used the website https://ThingSpeak.com. By using ThingSpeak, you can share your sensor data on their platform and visualize it on a graph along with timestamps. This enables you to conveniently access your sensor readings from any location worldwide.

Next step is creating a new channel on Thingspeak and getting and API key for uploading the data. 
![Alt text](images/thingspeak_img1.png)

You are now ready to run your code on the development board. To upload the code, follow these steps:

1. Open the Visual Studio Code with given code.
2. Replace the placeholders in the code with your actual SSID (WiFi name), WiFi password, and API key.
3. Make sure you have assembled the circuit according to the circuit diagram.
4. Connect the development board to your computer.
5. Select the appropriate board pin in the Raspberry Pi Pico.
6. Click on the 'Run' button to compile and run the code.
7. See and wait for the Raspberry Pi Pico to connect to the internet and send data to ThingSpeak.


# Putting Everything together
The setup of the device and the wiring is shown down below

![Alt text](images/breadboard_blueprint.png)

# Platform
For this project, I chose ThingSpeak because it is a free cloud service that meets my project's needs effectively. ThingSpeak offers user-friendly features for real-time data visualization on its online dashboard, enabling users to select from multiple display formats like diagrams and gauges. Moreover, it supports online data analysis through its channels, making data analysis straightforward and accessible.

# The code
```
import network
import time
import machine
import urequests
import dht

SSID = '' # WiFi internets username
PASSWORD = '' # internets password

# ThingSpeak settings
WRITE_API_KEY = ''  # Place API key from ThingSpeak
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# Function to connect to Wi-Fi
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    max_wait = 10
    while max_wait > 0:
        if wlan.status() == network.STAT_GOT_IP:
            print('Connected to Wi-Fi')
            print('IP Address:', wlan.ifconfig()[0])
            return True
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)
    
    print('Failed to connect to Wi-Fi')
    return False

# Function to send data to ThingSpeak
def send_to_thingspeak(temperature, humidity):
    try:
        url = f"{THINGSPEAK_URL}?api_key={WRITE_API_KEY}&field1={temperature}&field2={humidity}"
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak")
    except Exception as e:
        print("Failed to send data to ThingSpeak:", e)

# Main function
def main():
    # Connect to Wi-Fi
    if not connect_to_wifi(SSID, PASSWORD):
        return

    # Define the pin where the DHT11 data pin is connected (e.g., GPIO15)
    dht11_pin = machine.Pin(27)  # Change the pin number if needed

    # Initialize the DHT11 sensor
    dht11_sensor = dht.DHT11(dht11_pin)

    while True:
        try:
            # Measure temperature and humidity
            dht11_sensor.measure()
            temperature = dht11_sensor.temperature()
            humidity = dht11_sensor.humidity()
            print(f"Temperature: {temperature} C   Humidity: {humidity}%")
            
            # Send data to ThingSpeak
            send_to_thingspeak(temperature, humidity)
            
            # Add a delay before taking the next measurement
            time.sleep(15)  # ThingSpeak allows updates every 15 seconds for free accounts
        except OSError as e:
            print("Failed to read sensor:", e)

# Run the main function
main()
```

# Transmitting the data / connectivity
I opted to send data at hourly intervals to monitor the humidity levels in my room. This frequency is ideal for determining if the environment is too dry.

For wireless communication, I used WiFi because my microcontroller is positioned near my home router, eliminating the need for a longer-range protocol. WiFi also incurs no recurring costs, offers low latency, and has minimal bandwidth restrictions, making it the optimal choice.

To transmit the data, I used the Hypertext Transfer Protocol (HTTP). This protocol enables the sensor data to be sent to ThingSpeak. HTTP facilitates communication between a client and server using a request-response model. I specifically utilized the POST request method, which allows data to be sent to the server for creating or updating resources, such as publishing sensor readings.

# Presenting the data
The Thingspeak dashboard is configured with two data fields: one for humidity and one for temperature. Each field is accompanied by a diagram that displays the respective sensor values every 15 minutes. The humidity data is presented in percentages, while the temperature data is shown in Celsius.
![Alt text](images/thingspeak_temp.png)
![Alt text](images/thingspeak_humid.png)

# Finalizing the design

![Alt text](images/setup1.jpg)
![Alt text](images/setup2.jpg)

# Final thoughts

The project was successful, I managed to connect everything and send date to ThingSpeak. The programming with python was not hard, because I had written on it before. Connecting everything was also easy, because I also had some of the experience with Raspberry Pi Pico. And of course now I know that my room has enough humidity.
