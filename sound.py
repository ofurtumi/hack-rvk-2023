import pyaudio
import wave

def init_stream(filename):
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    return wf, stream, p

def write_stream(wave_file, stream, modifier, chunk_size = 1024):
    data = wave_file.readframes(chunk_size)
    if data != '':
        stream.write(data * modifier)


def killstream(stream, p):
    stream.close()
    p.terminate()

