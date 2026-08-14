from core.mqtt_client import MqttClient
from core.command_receiver import CommandReceiver
from core.sensors_exporter import SensorsExporter
from utils.initializer import load_config, init_all_sensors
import time
import os
import platform


BANNER = r"""                                                                            
.oPYo. .oPYo. o    o .oPYo. .oPYo.  .oPYo.    .oPYo.  .oPYo. o ooo.   .oPYo. .oPYo. 
8      8.     8b   8 8      8    8  8   `8    8   `8  8   `8 8 8  `8. 8    8 8.     
`Yooo. `boo   8`b  8 `Yooo. 8    8 o8YooP'   o8YooP' o8YooP' 8 8   `8 8      `boo   
    `8 .P     8 `b 8     `8 8    8  8   `b    8   `b  8   `b 8 8    8 8   oo .P     
     8 8      8  `b8      8 8    8  8    8    8    8  8    8 8 8   .P 8    8 8      
`YooP' `YooP' 8   `8 `YooP' `YooP'  8    8    8oooP'  8    8 8 8ooo'  `YooP8 `YooP' 
:.....::.....:..:::..:.....::.....::..:::..:::......::..:::.........:::....8 :.....:
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::8 :::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::..:::::::      
"""


def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


config = load_config()
sensors = init_all_sensors(config)

bme280_sensor = sensors["bme280"]
light_sensor = sensors["ltr559"]
microphone_sensor = sensors["sph0645"]
particulate_matter_sensor = sensors["pms5003"]
co2_sensor = sensors["scd30"]

command_receiver = CommandReceiver(
    temperature_sensor=bme280_sensor,
    pressure_sensor=bme280_sensor,
    humidity_sensor=bme280_sensor,
    light_sensor=light_sensor,
    microphone_sensor=microphone_sensor,
    particulate_matter_sensor=particulate_matter_sensor,
    co2_sensor=co2_sensor,
)

sensors_exporter = SensorsExporter(
    temperature_sensor=bme280_sensor,
    pressure_sensor=bme280_sensor,
    humidity_sensor=bme280_sensor,
    light_sensor=light_sensor,
    microphone_sensor=microphone_sensor,
    particulate_matter_sensor=particulate_matter_sensor,
    co2_sensor=co2_sensor,
)

MQTT_CLIENT = MqttClient(config["mqtt_broker"], config["mqtt_port"], command_receiver)
FETCH_INTERVAL_SECOND = config["update_interval"]
log_queue = ["---", "---", "---"]

try:
    while True:
        # get data
        data = sensors_exporter.export()
        
        # display
        clear_screen()

        print(BANNER)
        print(f"RUNNING | interval: {FETCH_INTERVAL_SECOND}s | broker: {config['mqtt_broker']}:{config['mqtt_port']}\n")        
        for key, value in data.items():
            print(f"  {key:<20} {value}")
        print("\nlog:")
        for i, log in enumerate(log_queue):
            prefix = "> " if i == len(log_queue) - 1 else "  "
            print(f"{prefix}{log}")

        # send data
        MQTT_CLIENT.send_data("sensors/data", data)
        
        # log
        timestamp = time.strftime("%H:%M:%S")
        log_queue.pop(0)
        log_queue.append(f"Data sent at {timestamp}")
        
        # sleep
        time.sleep(FETCH_INTERVAL_SECOND)
except KeyboardInterrupt:
    print("\nTerminating program...")
    MQTT_CLIENT.close()
    print("Done.")