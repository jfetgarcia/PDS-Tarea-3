# PDS-Tarea-3
Files in this repository
| File | Tooltip |
| --- | --- |
| analyze_effects.py | Reproduces effects by impulse response and convolving |
| analyze_song.py | Reads senal_misteriosa.wav and attemps to filter with autocorrelation method |
| cancion_filtrada.wav | Output filtered song from analyze_song.py |
| chirp_signal.py | Script which analyzes signal after passing through channel. Determines object distance, SONAR resolution and minimum chirp needed to detect object|
| efectos_fir.py | Reverb and eco effects for sound files |
| environment.yml | file to create conda enviroment |
| README.md | This file with details repository documentation |
| senal_misteriosa.wav | Input song for analyze_song.py |
| sonar_channel.py | Simulate wave passing through channel. Adds noise, delay and damping |
| Tarea-3_Señales-y-Sistemas-en-Tiempo-Discreto-2.pdf| Report pdf on results for work |


## Dependencies
For a reproducible enviroment Conda Miniforge was used. For Linux Ubuntu, the following command was used:
```
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

## Running scripts
1.  Run the enviroment script to setup dependencies necessary for both scripts
```
conda env create -f environment.yml
conda activate pds-tarea3
```
2. Running scripts example
```
python3 chirp_signal.py
```
3. Exit enviroment
```
conda deactivate
```
### Script: chirp_signal.py
This script runs a SONAR chirp signal through a simulated water channel and estimates distance to an object based on a returned signal.

Run the script with
```
python3 chirp_signal.py
```
Expected output
```
Atraso estimado: 19200 muestras
Atraso temporal: 200.0 ms
Distancia estimada: 150.0 m
Resolucion espacial: 0.075 m
SNR supera 10 dB a partir de 2.0208333333333273 ms
```
Also 3 graphs are created. 
* The sent/recieved signal correlation. 
* The example chirp signal. 
* The SNR vs. chirp duration


### Script: sonar_channel.py
**This file is not meant to work as an independent script. Do not run on its own**

### Script: analyze_song.py
This script attempts to filter the senal_misteriosa.wav and writes the result to cancion_filtrada.wav

Run the script with
```
python3 analyze_song.py
```

Expected ouptut is the wav file and the following terminal output:
```
Período estimado: 490 muestras
Tiempo del período: 0.0306 s
```
### Script: analyze_effects.py
This script recreates reverb and eco effects from efectos_fir.py. This is done
by generating the impulse response and applying convolving with input signals

Run the script with
```
python3 analyze_effects.py
```
Expected output
```
SNR cascada: 302.85 dB
Error máximo cascada: 5.551115123126e-16
SNR sistema equivalente: 303.73 dB
Error máximo sistema equivalente: 6.106226635438e-16
```
### Script: efectos_fir.py
**This file is not meant to work as an independent script. Do not run on its own**

## Troubleshooting
When installing the conda enviroment. The base enviroment might not activate. This can
result in the `conda` commands not being recognized. This can be fixed by running the
conda binary as follows:
```
<PATH TO MINIFORGE INSTALL>/miniforge3/bin/conda init
```
The terminal should show `(base)` at the start of the line if the conda base
enviroment was succesfully enabled.
