
# Serial-MQTT-Bridge

Windows app untuk melakukan bridging data melalui komunikasi serial (USB), agar MCU bisa publish & subscribe ke atau dari broker MQTT(SSL/TLS).
Kalau mau pakai koneksi non-ssl/tls run aja aplikasinya lewat python, edit dulu skripnya di hapus atau di jadiin comment di bagian ini :
    
    mqttc.tls_set()

Cek appnya disini :
        
[Serial-MQTT-Bridge/dist/Serial-MQTT-Bridge.exe](https://github.com/robertrullyp/Serial-MQTT-Bridge/blob/main/dist/Serial-MQTT-Bridge.exe)

Python Codenya disini :

[Serial-MQTT-Bridge.py](https://github.com/robertrullyp/Serial-MQTT-Bridge/blob/main/Serial-MQTT-Bridge.py)

Berhubung board MatekF405-STD adalah board untuk Flight Controller yang sudah ada BMP280 jadi bisa dimanfaatkan, buat contoh aja. Untuk contoh sketch arduino bisa cek Serial-MQTT-Bridge/STM32F4(MatekF405STD)-blink&SensorJSON.ino disesuaikan aja dan install sendiri beberapa library arduino yang dibutuhkan. tekan CTRL+C untuk menghentikan aplikasi dan keluar
    ![Serial-MQTT-Bridge](https://github.com/robertrullyp/Serial-MQTT-Bridge/assets/12167355/dd9ef314-8c7c-47bb-8f70-a47de60e9fc5)

cek juga tools mqtt yg bermanfaat buat ngeliat struktur topic mqtt : [MQTT EXPLORER](https://mqtt-explorer.com/)

![TestSerial-MQTT-Bridge](https://github.com/robertrullyp/Serial-MQTT-Bridge/assets/12167355/4769c3d6-c8ed-49a5-a8b8-2b88f6e49a7d)

