## lightberryAPI 

a lightweight, RESTful focused, `MicroPython` web framework & server for `RaspberryPi Pico W`,
successor of [strawberryAPI](https://github.com/zNitche/strawberryAPI).

### Environment
- Raspberry Pi Pico W 2022 version
- Micropython for Rpi Pico W - v1.22.2 stable

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

### How to use it

#### Build python package 
(doesn't seem to work with Micropython on RP2040)
```
python3 -m build --sdist
```

#### As git submodule

In order to use `lightberryAPI` in your project without keeping whole 
codebase in repo, framework should be added as `git submodule`.

In your project root directory:

1. Add `lightberryAPI` as git submodule.
```
git submodule add --name lightberry -b production https://github.com/zNitche/lightberryAPI ./lightberry
```

2. Create `lightberry_config.json`.
```
wget -O lightberry_config.json https://raw.githubusercontent.com/zNitche/lightberryAPI/main/lightberry_config.template.json
```

Note that `App` section can be extended, all values passed there
will be available in `App.config`.

3. Example project structure and app setup can be found in:
- `main.py`
- `routes/`

4. Flash microcontroller and you are good to go.

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

2. Get lightberryAPI
```
git clone https://github.com/zNitche/lightberryAPI.git --branch=production
```

3. Prepare module
```
mv lightberryAPI lightberry
rm -rf lightberry/.git
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
cp -r ../lightberry ports/rp2/modules/
```

8. Build firmware
```
make -C ports/rp2 BOARD=RPI_PICO_W
```

Flash Pico (using BOOTSEL button) with newly created `firmware.uf2`
```
micropython/ports/rp2/build-RPI_PICO_W/firmware.uf2
```
Now connect via REPL, to verify if module has been included correctly type:
```
import lightberry
```

No errors, we are good to go

##### Types hints
In order to have proper code hints/autocompletion working we can do two things:
1. Copy content of `lightberry` to `[YOUR_VENV_DIR]/lib/python[VERSION]/site-packages/lightberry`

or

2. Generate `.pyi` files using `mypy`. This approach is described below,
the only difference is, target directory which in this case should be
```
out/lightberry -> [YOUR_VENV_DIR]/lib/python[VERSION]/site-packages/lightberry
```

##### Types hints (PyCharm + MicroPython Plugin)
To enjoy code autocompletion we have to generate `.pyi` files
for `lightberryAPI`

1. Get `MyPy`
```
pip3 install mypy
```

2. Generate `.pyi` files
```
mkdir out
stubgen lightberry
```

3. Copy content of `out/lightberry` to `[PYCHARM_DIR]/intellij-micropython/typehints/micropython/lightberry`

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

### Development

packages in `requirements.txt` used for `MicroPython` development 
using `PyCharm Micropython Plugin`.

```
pip3 install -r requirements.txt
```

Because repl in `Micropython plugin 1.4.0` doesn't seem to work with `Pycharm CE 2024.1.3`,
added `rshell` to replace it.

```
> rshell
> repl
```
