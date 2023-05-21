from genki_signals.system import System
from genki_signals.sources import WaveSource
from genki_wave.discover import run_discover_bluetooth
from sound import *
from time import sleep

def wave_init(ble_address = "F8:17:0E:EF:AB:82"):
    ws = WaveSource(ble_address)
    system = System(ws, [])
    system.start()
    return ws, system

def wave_kill(ws, system):
    ws.stop()
    system.stop()


def wave_check(ws, system, state, cooldown):
    if (cooldown <= 0 and ws.latest_point != None):
        points = ws.latest_point["linacc"] < -4.5
        if any(points):
            # subprocess.run(["ffplay", "-v", "0", "-nodisp", "-autoexit", "punch.mp3"])
            if state:
                state = False
            else:
                state = True
            print(points)
            cooldown = 10

    return state, cooldown - 1

# if __name__ == "__main__":
#     ws, system = wave_init()
#     state, cooldown = False, 0
#     try:
#         while True:
#             state, cooldown = wave_check(ws, system, state, cooldown)
#             print(state, cooldown)
#     except KeyboardInterrupt:
#         wave_kill(ws, system)
#

