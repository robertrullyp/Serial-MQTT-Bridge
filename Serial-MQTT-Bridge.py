import sys, time, signal
import serial
import paho.mqtt.client as mqtt
import json

################################################################
# Global script variables.
serialc = None
client = None
################################################################
################################################################
# Attach a handler to the keyboard interrupt (control-C).
def _sigint_handler(signal, frame):
    print("")
    print("Keyboard interrupt caught, closing down...")
    if serialc is not None:
        serialc.close()
    if client is not None:
        client.loop_stop()
    time.sleep(1.5)
    sys.exit(0)
signal.signal(signal.SIGINT, _sigint_handler)        
################################################################
################################################################
print("""\
Parameter berikut harus disesuaikan sebelum menggunakan program..
Nilai parameter diperlukan dalam konfigurasi untuk menjalankan program
Isi dengan benar, Pastikan pengisian sesuai dengan format penulisan..!
""")
################################################################
################################################################
def printserial ():
    import serial.tools.list_ports
    print("All available serial ports:")
    for p in serial.tools.list_ports.comports():
        print(" ", p.device)
################################################################
################################################################
def mqttparam(txtinput):
    while True:
        param = input(txtinput) # type: ignore
        if param != "":
            break
    return param
################################################################
################################################################
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT with result code {reason_code}")
    client.subscribe(mqtt_sub)
    return
def on_message(client, userdata, msg):
    print("Received from MQTT: "+msg.topic+" "+str(msg.payload))
    if serialc is not None and serialc.is_open:
        serialc.write(msg.payload + b'\n')
        print(f"Sent to Serial {serial_portname}: {msg.payload}")
        print("")
    return
################################################################
################################################################
if __name__ == "__main__":
    mqtt_hostname = mqttparam('MQTT Server Hostname (ex: iotsmarthome.my.id): ')
    mqtt_port = mqttparam('MQTT Server Port (ex: 8883): ')
    while True:
        try:
            mqtt_port = int(mqtt_port)
        except ValueError:
            print("MASUKKAN ANGKA PADA SERVER PORT DAN TIDAK BOLEH KOSONG...!!")
            input("Press Enter to Continue...")
            mqtt_port = mqttparam('MQTT Server Port (ex: 8883): ')
            continue
        break
    mqtt_pub = mqttparam('MQTT Publish Topic (ex: usertest): ')
    mqtt_sub = mqttparam('MQTT Subscribe Topic (ex: $SYS/#): ')
    mqtt_username = input('MQTT Username: ')
    mqtt_password = input('MQTT Password: ')
    while True:
        serial_portname = input('Serial Port (ex: COM23): ')
        if serial_portname == '':
            printserial()
            continue
            #sys.exit(0)
        try:
            serialc = serial.Serial(serial_portname, baudrate=115200, timeout=2.0)
        except serial.SerialException:
            print("MASUKKAN SERIAL PORT DENGAN BENAR...!!")
            printserial()
            # serial_portname = input('Serial Port (ex: COM23): ')
            continue
        break
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) # type: ignore
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.tls_set()
    mqttc.username_pw_set(mqtt_username, mqtt_password)
    print(f"Connecting To MQTT.....")
    mqttc.connect_async(mqtt_hostname, mqtt_port, 60)
    mqttc.loop_start()
    #mqttc.loop_forever()
    print(f"Connecting To Serial Port {serial_portname}.....")
    time.sleep(0.2)  # wait briefly for the Arduino to complete waking up
    print(f"Entering Arduino event loop for Serial Port {serial_portname}.  Enter Control-C to quit.")
    while(True):
        try:
            # serinput = serialc.readline().decode(encoding='ascii',errors='ignore').rstrip()
            serinput = serialc.readline().rstrip()
        except serial.SerialException:
            print("Koneksi Serial Terputus..!")
            time.sleep(3)
        if len(serinput) == 0:
            print("Serial device timed out, no data received.")
        else:
            print(f"Received from serial device: {serinput}")
            json_data = json.loads(serinput.decode(encoding='utf-8',errors='ignore'))
            print(json.dumps(json_data, indent=2))
            if mqttc.is_connected():
                # mqttc.publish(topic=mqtt_pub, payload=serinput)
                mqttc.publish(topic=mqtt_pub, payload=json.dumps(json_data, indent=2))
                print(f"Published to {mqtt_pub}: {serinput}")
                print("")
################################################################
