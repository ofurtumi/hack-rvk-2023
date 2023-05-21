from genki_signals.system import System
from genki_signals.sources import WaveSource
from genki_wave.discover import run_discover_bluetooth
from time import sleep
from sound import *
from riff import Riff
import subprocess

ble_address = ""
if input("Use default address? (y/n): ") == "y":
    # ble_address = "CD:05:D8:8A:2F:D0" 
    ble_address = "F8:17:0E:EF:AB:82" 
else:
    run_discover_bluetooth()
    exit()

ws = WaveSource(ble_address)

wf, stream, p = init_stream("JH.wav")
system = System(ws, [])
system.start()
aerostar = False
forever = True
cooldown = 0
try:
    while forever: 
        if aerostar:
            write_stream(wf, stream, 2)
        else:
            write_stream(wf, stream, 1)

        if (cooldown <= 0 and ws.latest_point != None):
            points = ws.latest_point["linacc"] < -4.5
            if any(points):
                # subprocess.run(["ffplay", "-v", "0", "-nodisp", "-autoexit", "punch.mp3"]) 
                if aerostar:
                    aerostar = False
                    print("aerostar")
                else:
                    aerostar = True
                    print("ratsorea")
                print(points)
                cooldown = 50

        print(cooldown)
        cooldown = cooldown - 1


except KeyboardInterrupt:
    print("Exiting...")
    killstream(stream, p)
    forever = False
    system.stop()
    exit()
