## lightberryAPI 

a lightweight `MicroPython` web framework & server for `RaspberryPi Pico W`,
successor of [strawberryAPI](https://github.com/zNitche/strawberryAPI).

### Environment
- Raspberry Pi Pico W 2022 version
- Micropython for Rpi Pico W - v1.22.2 stable

##### Note
I have recently tested if `ESP32` can run `lightberryAPI`, and as I expected, it worked.
One thing is to disable `BLINK_LED` in config. 

### Features
- async web server, supporting 2 modes:
  - client.
  - host (Wi-Fi hotspot).
- routers based routing (similar to `flask` blueprints).
- url and query / search parameters parsing.
- async background tasks.
- threading background tasks (experimental).
- generator based file responses.
- separated json configs for app and server.
- support for SSL/TLS (HTTPS).
- debug logging.
- turning WLAN on/off for power saving.
- auto Wi-Fi reconnect.

### Project Goals
- build universal tool I can use in my future projects.
- complete `strawberryAPI` overhaul:
  - full async routing.
  - replacement of interrupts based background tasks with async schedulers.
  - removed built in templates engine.
- implementation of better and more user / git friendly configs handling.
- files streaming, with serving react compressed apps in mind.
- implementation of better routing, with `catch_all` routes and after
requests handling.
- type hints for all modules.
- support for SSL/TLS

### Development
packages in `requirements.txt` are used for development / build
```
pip3 install -r requirements.txt
```

#### Code autocompletion
To enjoy code autocompletion and type hints `lightberryAPI` can be installed as python package.

Add following line to your `requirements.txt`
```
lightberry @ git+https://github.com/zNitche/lightberryAPI.git
```

version can be specified
```
lightberry @ git+https://github.com/zNitche/lightberryAPI.git@v1.2.4
```

#### Remote Shell
for flashing pico you can use `rshell`

enter REPL
```
rshell -p /dev/ttyUSBX
repl
```

flash
```
rshell -p /dev/ttyUSBX -f commands/flash
```

clear all files
```
rshell -p /dev/ttyUSBX -f commands/wipe
```

### How to use it

#### Get package from Github release

1. Get `.zip` package (replace `<VERSION>` with release number, for instance `v1.3.0`)
```
wget -O lightberry.zip https://github.com/zNitche/lightberryAPI/releases/download/<VERSION>/lightberry-<VERSION>.zip
```

2. Unpack archive and add its content to your project (don't forget to include it in `.gitignore`)
```
unzip lightberry.zip
cp -r lightberry <PROJECT_PATH>/lightberry
```

3. Flash microcontroller and you are good to go.

#### As a MicroPython frozen module

As far as I know it is the fastest method to work with, 
you don't have to flash whole library + your project files every time you want
to test your changes. We are gonna to build MicroPython from source with 
`lightberryAPI` included as module, so let's get down to business.

1. Install required dependencies + tools
```
sudo apt update
sudo apt install cmake build-essential
sudo apt install gcc-arm-none-eabi libnewlib-arm-none-eabi
```

2. Get lightberryAPI (replace `<VERSION>` with release number, for instance `v1.3.0`)
```
wget -O lightberry.zip https://github.com/zNitche/lightberryAPI/releases/download/<VERSION>/lightberry-<VERSION>.zip
```

3. Prepare package
```
unzip lightberry.zip
rm lightberry.zip
```

4. Get MicroPython
```
git clone https://github.com/micropython/micropython.git --branch v1.22.2
```

5. Init submodules
```
cd micropython
make -C ports/rp2 BOARD=RPI_PICO_W submodules
```

6. Build cross-compiler
```
make -C mpy-cross
```

7. Move `lightberry` directory to target destination
```
cp -r ../lightberry ports/rp2/modules/lightberry
```

8. Build firmware
```
make -C ports/rp2 BOARD=RPI_PICO_W
```

Flash Pico (using BOOTSEL button) with newly created `firmware.uf2`
```
micropython/ports/rp2/build-RPI_PICO_W/firmware.uf2
```
Now connect via REPL, to verify if module has been included correctly, type:
```
import lightberry
```

No errors, we are good to go

### Examples
- `main.py` - app and server setup.
- `routes/` - routes setup + workflow.
- `tasks.py` - background tasks.
- `lightberry_config.template.json` - config template.

Note that `App` section can be extended, all values passed there
will be available in `current_app.config`.

### Extras
#### SSL / TLS

1. Generate cert + key
```
openssl req -x509 -newkey rsa:2048 -nodes -out cert.pem -keyout key.pem -days 365
```

2. Convert `.pem` to `.der` for micropython ssl module
```
openssl x509 -in cert.pem -out cert.der -outform DER
openssl rsa -in key.pem -out key.der -outform DER
```

3. Update `lightberry_config.json`
```
"CERT_FILE": "/cert.der",
"CERT_KEY": "/key.der"
```

lightberryAPI comes with build in kind of reverse proxy (here called ssl proxy) to
redirect requests from `SERVER_PORT` to port no. 443 (HTTPS)
