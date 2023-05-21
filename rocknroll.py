import time
import soundfile as sf
import pyaudio
from pedalboard import Gain, Pedalboard, Compressor, Distortion, Reverb, Chorus, Phaser, Delay, PitchShift
from ring import wave_init, wave_kill, wave_check

# Effect presets
compressor = Compressor(threshold_db=-18, ratio=2, attack_ms=10, release_ms=100)
distortion = Distortion(drive_db=25)
gain = Gain(gain_db=-5)
reverb = Reverb()
chorus = Chorus()
phaser = Phaser(rate_hz=1.0, depth=0.5, centre_frequency_hz=1300.0, feedback=0.0, mix=0.5)
delay = Delay()
pitchshift = PitchShift(semitones=-0.000005)


# Global variables
pedalboard = Pedalboard()

input_file = 'JH.wav'
audio, sample_rate = sf.read(input_file)
originalaudio = audio
current_pos = 0
chunk_size = 1024

ring_swing = False
ring_effects = False

# Wave ring variables
ws, system = wave_init()
state, cooldown = False, 0

# PyAudio callback function
def callback(in_data, frame_count, time_info, status):
    global current_pos, audio, pedalboard, sample_rate

    end_pos = current_pos + frame_count
    chunk_audio = audio[current_pos:end_pos]
    processed_audio = pedalboard(chunk_audio, sample_rate)
    current_pos = end_pos

    return processed_audio.tobytes(), pyaudio.paContinue

# PyAudio initialization
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=audio.shape[1],
                rate=sample_rate,
                output=True,
                stream_callback=callback,
                frames_per_buffer=chunk_size)


stream.start_stream()
pedalboard.append(gain)
pedalboard.append(distortion)

# Play loop
try:
    while current_pos < len(audio):
        state, cooldown = wave_check(ws, system, state, cooldown)
        ring_swing = state
        if ring_swing and not ring_effects:
            ring_effects = True
            pedalboard.append(compressor)
            pedalboard.remove(gain)
            pedalboard.remove(distortion)

        if not ring_swing and ring_effects:
            ring_effects = False
            pedalboard.remove(compressor)
            pedalboard.append(gain)
            pedalboard.append(distortion)


        if not stream.is_active():
            break
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program interrupted by the user.")

wave_kill(ws, system)
stream.stop_stream()
stream.close()

p.terminate()
