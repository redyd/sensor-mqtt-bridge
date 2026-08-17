from core.mqtt_client import MqttClient
from core.command_receiver import CommandReceiver
from core.sensors_exporter import SensorsExporter
from utils.initializer import load_config, init_all_sensors
import time
import os
import platform


BANNER = r'''                                                                            
   ___     ___    _  _     ___     ___     ___              ___     ___     ___     ___     ___     ___   
  / __|   | __|  | \| |   / __|   / _ \   | _ \     o O O  | _ )   | _ \   |_ _|   |   \   / __|   | __|  
  \__ \   | _|   | .` |   \__ \  | (_) |  |   /    o       | _ \   |   /    | |    | |) | | (_ |   | _|   
  |___/   |___|  |_|\_|   |___/   \___/   |_|_\   TS__[O]  |___/   |_|_\   |___|   |___/   \___|   |___|  
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
'''

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"

WIDTH = 58
SENSOR_KEYS = [
    "temperature",
    "pressure",
    "humidity",
    "light",
    "sound_level",
    "particulate_matter",
    "co2",
]


def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_header(interval, broker, port, status):
    state = "pause" if status else "running"
    print(BANNER)
    print(f"{DIM}status: {state} | interval: {interval}s | broker: {broker}:{port}{RESET}")
    print(f"{CYAN}{'-' * WIDTH}{RESET}")


def print_sensors_table(values):
    print(f"{BOLD}{'SENSOR':<20}{'RAW':>12}{'SMOOTH':>12}{'SCORE':>12}{RESET}")
    print(f"{CYAN}{'-' * WIDTH}{RESET}")

    for key in SENSOR_KEYS:
        reading = values.get(key, {})
        raw_value = reading.get("raw", "-")
        smooth_value = reading.get("smooth", "-")
        score = reading.get("score", "-")
        print(
            f"{key:<20}"
            f"{format_display_value(raw_value):>12}"
            f"{format_display_value(smooth_value):>12}"
            f"{format_display_value(score):>12}"
        )

    print(f"{CYAN}{'-' * WIDTH}{RESET}")


def format_display_value(value):
    if isinstance(value, (int, float)):
        return f"{value:.2f}"
    return str(value)


def print_send_status(send_ok, score):
    status_color = GREEN if send_ok else RED
    print(f"MQTT send: {status_color}{'OK' if send_ok else 'FAIL'}{RESET} | score: {format_display_value(score)}")


def print_log(log_queue):
    print(f"\n{BOLD}LOG{RESET}")
    print(f"{CYAN}{'-' * WIDTH}{RESET}")
    for i, log in enumerate(log_queue):
        prefix = ">" if i == len(log_queue) - 1 else " "
        print(f" {prefix} {log}")


def send_sensor_data(mqtt_client, payload):
    return mqtt_client.send_data("sensors/data", payload)


def update_fetch_interval(new_interval):
    global FETCH_INTERVAL_SECOND
    FETCH_INTERVAL_SECOND = new_interval
    return FETCH_INTERVAL_SECOND


def toogle_pause(new_state):
    global PAUSE
    PAUSE = new_state


FETCH_INTERVAL_SECOND = None
PAUSE = False


def main():
    global FETCH_INTERVAL_SECOND

    config = load_config()
    sensors = init_all_sensors(config)

    bme280_sensor = sensors["bme280"]
    light_sensor = sensors["ltr559"]
    microphone_sensor = sensors["sph0645"]
    particulate_matter_sensor = sensors["pms5003"]
    co2_sensor = sensors["scd30"]
    lmt84 = sensors["lmt84"]

    sensors_exporter = SensorsExporter(
        temperature_sensors=[bme280_sensor, lmt84, co2_sensor],
        pressure_sensors=[bme280_sensor],
        humidity_sensors=[bme280_sensor, co2_sensor],
        light_sensors=[light_sensor],
        microphone_sensors=[microphone_sensor],
        particulate_matter_sensors=[particulate_matter_sensor],
        co2_sensors=[co2_sensor],
    )

    FETCH_INTERVAL_SECOND = config["update_interval"]

    command_receiver = CommandReceiver(
        update_interval_callback=update_fetch_interval,
        toggle_pause_callback=toogle_pause
    )

    mqtt_client = MqttClient(config["mqtt_broker"], config["mqtt_port"], command_receiver)
    log_queue = ["---", "---", "---"]

    try:
        while True:
            clear_screen()
            print_header(FETCH_INTERVAL_SECOND, config["mqtt_broker"], config["mqtt_port"], PAUSE)

            if PAUSE:
                while PAUSE:
                    time.sleep(0.5)

            payload = sensors_exporter.export()
            values = payload["values"]

            print_sensors_table(values)

            send_ok = send_sensor_data(mqtt_client, payload)
            print_send_status(send_ok, payload.get("score", "-"))

            timestamp = time.strftime("%H:%M:%S")
            log_queue.pop(0)
            log_queue.append(f"Data sent at {timestamp}" if send_ok else f"Send failed at {timestamp}")

            print_log(log_queue)

            time.sleep(FETCH_INTERVAL_SECOND)
    except KeyboardInterrupt:
        print("\nTerminating program...")
        mqtt_client.close()
        print("Done.")


if __name__ == "__main__":
    main()
