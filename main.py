import numpy as np
import tkinter as tk
import threading
import sounddevice as sd
import scipy.io.wavfile as wavf

audiodevice = 35 #python -m sounddevice
path_to_audio = "test_audio.wav"
fs_hz, audio = wavf.read(path_to_audio, mmap=False)
start_idx = 0
end_idx   = 0
end = threading.Event()
end.clear()
angle = .0

def audio_callback(indata, outdata, frames, time, status):
    global start_idx
    global end_idx
    outdata.fill(0)
    if status:
        print(status)
    if end_idx < len(audio):
        end_idx = min([start_idx+frames, len(audio)])
        outdata[:end_idx-start_idx, 0] = np.sin(angle)*audio[start_idx:end_idx]
        outdata[:end_idx-start_idx, 1] = np.cos(angle)*audio[start_idx:end_idx]
        start_idx += frames
    else:
        start_idx = 0
        end_idx   = 0
        end.set()

stream = sd.Stream(callback=audio_callback,
                   dtype=audio.dtype,
                   device=audiodevice,
                   channels=2,
                   samplerate=int(fs_hz))

def change_panorama(set_angle_deg):
    global angle
    angle = ((float(set_angle_deg)+45)/180)*np.pi

with stream:
    window = tk.Tk()
    window.title('audio-panner')
    window.geometry("400x100")

    scale = tk.Scale(window,
                     from_=-45,
                     to=45,
                     length=380,
                     orient=tk.HORIZONTAL,
                     command=change_panorama)
    scale.set(0)
    scale.pack()


    window.mainloop()