import math
import time
import numpy as np
import keyboard
import soundfile as sf
import pyaudio
from pedalboard import Plugin, Gain, Pedalboard, Compressor, Distortion, Reverb, Chorus, Phaser, Delay, PitchShift

compressor = Compressor(threshold_db=-18, ratio=2, attack_ms=10, release_ms=100)
distortion = Distortion(drive_db=25)
gain = Gain(gain_db=-20)
reverb = Reverb(room_size=0.75, damping=0.2)
chorus = Chorus(rate_hz=5.0, depth=2, centre_delay_ms=7.0, feedback=0.7, mix=0.5)
phaser = Phaser(rate_hz=1.0, depth=0.5, centre_frequency_hz=1300.0, feedback=0.0, mix=0.5)
delay = Delay(delay_seconds=2, feedback=0.9, mix=0.5)
pitchshift = PitchShift(semitones=-0.000005)

synthcompressor = Compressor(threshold_db=-20, ratio=4)
synthdistortion = Distortion(drive_db=18)
synthreverb = Reverb(room_size=0.8, damping=0.5)

pedalboard = Pedalboard()
# pedalboard.append(compressor)
# pedalboard.append(distortion)
# pedalboard.append(reverb)

# pedalboard.append(chorus)
# pedalboard.append(phaser)
# pedalboard.append(pitchshift)

input_file = 'The Jimi Hendrix Experience - All Along The Watchtower (Official Audio).wav'
audio, sample_rate = sf.read(input_file)
originalaudio = audio
current_pos = 0
chunk_size = 1024


#def apply_tanh_effect(audio_data, gain=200, volume=0.10):
    #audio_data = np.tanh(audio_data * gain) * volume
    #return audio_data


def apply_tremolo_effect(audio_data, sample, depth=0.4, rate=15):
    t = np.linspace(0, len(audio_data) / sample, len(audio_data), False)
    tremolo_modulation = 1 + depth * np.sin(2 * np.pi * rate * t)
    synthesized_data = audio_data * tremolo_modulation[:, np.newaxis]
    return synthesized_data


def apply_synth_effect(audio_data, gain=200, volume=0.10):
    audio_data = np.tanh(audio_data * gain) * volume
    return audio_data


is_shift_pressed = False
is_alt_pressed = False
is_ctrl_pressed = False


def on_press(key):
    global is_shift_pressed
    global is_alt_pressed
    global is_ctrl_pressed
    global audio
    if key.name == 'shift' and not is_shift_pressed:
        is_shift_pressed = True
        audio = apply_tremolo_effect(audio, sample_rate)
    if key.name == 'alt' and not is_alt_pressed:
        is_alt_pressed = True
        pedalboard.append(distortion)
        pedalboard.append(gain)
        # pedalboard.append(delay)
    if key.name == 'ctrl' and not is_ctrl_pressed:
        is_ctrl_pressed = True
        pedalboard.append(synthreverb)
        pedalboard.append(synthcompressor)
        pedalboard.append(synthdistortion)


def on_release(key):
    global is_shift_pressed
    global is_alt_pressed
    global is_ctrl_pressed
    global audio
    if key.name == 'shift' and is_shift_pressed:
        is_shift_pressed = False
        audio = originalaudio
    if key.name == 'alt' and is_alt_pressed:
        is_alt_pressed = False
        pedalboard.remove(distortion)
        pedalboard.remove(gain)
        # pedalboard.remove(delay)
    if key.name == 'ctrl' and is_ctrl_pressed:
        is_ctrl_pressed = False
        pedalboard.remove(synthreverb)
        pedalboard.remove(synthcompressor)
        pedalboard.remove(synthdistortion)


keyboard.on_press_key('shift', on_press)
keyboard.on_release_key('shift', on_release)

keyboard.on_press_key('alt', on_press)
keyboard.on_release_key('alt', on_release)

keyboard.on_press_key('ctrl', on_press)
keyboard.on_release_key('ctrl', on_release)


def callback(in_data, frame_count, time_info, status):
    global current_pos, audio, pedalboard, sample_rate

    end_pos = current_pos + frame_count
    chunk_audio = audio[current_pos:end_pos]
    processed_audio = pedalboard(chunk_audio, sample_rate)
    current_pos = end_pos

    return processed_audio.tobytes(), pyaudio.paContinue


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=audio.shape[1],
                rate=sample_rate,
                output=True,
                stream_callback=callback,
                frames_per_buffer=chunk_size)

stream.start_stream()

try:
    while current_pos < len(audio):
        if not stream.is_active():
            break
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program interrupted by the user.")

stream.stop_stream()
stream.close()

p.terminate()
