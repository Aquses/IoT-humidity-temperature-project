import network # type: ignore
import time
import machine # type: ignore
import urequests # type: ignore
import dht # type: ignore

SSID = 'Čikis'
PASSWORD = '!cikis7A9$,t8j$;'

# ThingSpeak settings
WRITE_API_KEY = 'X400QW9MTIO3SSKT'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

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
        time.sleep(5)
    
    print('Failed to connect to Wi-Fi')
    return False

def send_to_thingspeak(temperature, humidity):
    try:
        url = f"{THINGSPEAK_URL}?api_key={WRITE_API_KEY}&field1={temperature}&field2={humidity}"
        response = urequests.get(url)

        print("HTTP/1.1", response.status_code, response.reason)
        print(f"Date: {response.headers.get('Date')}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Content-Length: {response.headers.get('Content-Length')}")
        print(f"Connection: {response.headers.get('Connection')}")
        print(f"Status: {response.status_code} {response.reason}")
        print(f"Cache-Control: {response.headers.get('Cache-Control')}")
        print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        print(f"Access-Control-Max-Age: {response.headers.get('Access-Control-Max-Age')}")
        print(f"X-Request-Id: {response.headers.get('X-Request-Id')}")

        response.close()
    except Exception as e:
        print("Failed to send data to ThingSpeak:", e)

def main():
    if not connect_to_wifi(SSID, PASSWORD):
        return

    dht11_pin = machine.Pin(27)
    dht11_sensor = dht.DHT11(dht11_pin)

    while True:
        try:
            dht11_sensor.measure()
            temperature = dht11_sensor.temperature()
            humidity = dht11_sensor.humidity()
            print(f"\nTemperature: {temperature} C, Humidity: {humidity}%")
            
            send_to_thingspeak(temperature, humidity)
            time.sleep(7200)
        except OSError as e:
            print("Failed to read sensor:", e)

main()
