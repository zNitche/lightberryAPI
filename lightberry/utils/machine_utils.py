import machine
import time


def get_onboard_led():
    onboard_led = machine.Pin("LED", machine.Pin.OUT)

    return onboard_led


def toggle_onboard_led():
    led = get_onboard_led()
    led.toggle()


def blink_onboard_led(pause_duration=0.3, blinks=1):
    led = get_onboard_led()

    if led.value():
        led.off()

    for _ in range(blinks):
        led.on()
        time.sleep(pause_duration)
        led.off()

    led.on()


def create_timer():
    return machine.Timer()


def init_periodic_timer(timer, period, cb):
    timer.init(period=period, mode=machine.Timer.PERIODIC, callback=lambda t: cb())
