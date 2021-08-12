import numpy as np
import threading
import sounddevice as sd
import scipy.io.wavfile as wavf
import dash
import dash_html_components as html
import dash_core_components as dcc

audiodevice = 35 #python -m sounddevice
path_to_audio = "test_audio.wav"
fs_hz, audio = wavf.read(path_to_audio, mmap=False)
start_idx = 0
end_idx   = 0
end = threading.Event()
end.clear()
angle = .0
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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

def change_panorama(set_angle_deg, n_clicks):
    global angle
    if n_clicks > 0:
        stream.start()
    angle = ((float(set_angle_deg)+45)/180)*np.pi


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
                        dcc.Slider(
                            id='slider',
                            min=-45,
                            max=45,
                            step=0.5,
                            value=0,
                        ),
                        html.Div(id='slider-output-container'),
                        html.Button('Play', id='play-val', n_clicks=0),
                        ])


@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('slider', 'value'),
     dash.dependencies.Input('play-val', 'n_clicks')])
def update_output(value, n_clicks):
    change_panorama(value, n_clicks)

app.run_server(debug=True)
