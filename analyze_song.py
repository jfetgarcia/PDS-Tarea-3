import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs, audio = wavfile.read("senal_misteriosa.wav")
dtype_original = audio.dtype
bits_por_muestra = dtype_original.itemsize * 8

audio = audio.astype(np.float64)

# Eliminar nivel DC
audio -= np.mean(audio)

audio /= max(np.max(np.abs(audio)), 1e-12)

M = len(audio)

# Buscar periodicidades hasta 1 segundo
max_desplazamiento= min(fs, M // 2)

correlacion = np.zeros(max_desplazamiento + 1)

for n in range(max_desplazamiento + 1):
    correlacion[n] = np.dot(audio[n:], audio[:M-n]) / M

# Normalizar para visualizar
correlacion /= max(correlacion[0], 1e-12)

# Ignorar retardos menores a 10 ms
min_atraso = int(0.01 * fs)

N0 = min_atraso + np.argmax(correlacion[min_atraso:])

T0 = N0 / fs

print(f"Período estimado: {N0} muestras")
print(f"Tiempo del período: {T0:.4f} s")

# Cantidad de períodos a promediar
K = 5

# Crear filtro de peine
h = np.zeros((K - 1) * N0 + 1)

h[::N0] = 1 / K

# Aplicar convolución
# FFT no es necesaria
audio_filtrado = np.convolve(audio, h, mode="full")

# Descartar transitorio inicial
inicio = (K - 1) * N0

audio_filtrado = audio_filtrado[inicio:inicio + len(audio) - inicio]

# Normalizar amplitud al rango [-1, 1]
audio_filtrado = audio_filtrado / max(
    np.max(np.abs(audio_filtrado)), 1e-12
)

# Convertir al formato original
if np.issubdtype(dtype_original, np.integer):

    info = np.iinfo(dtype_original)

    if np.issubdtype(dtype_original, np.unsignedinteger):
        # PCM sin signo, por ejemplo uint8
        centro = (info.max + 1) / 2
        audio_guardar = np.clip(
            np.round(audio_filtrado * (centro - 1) + centro),
            info.min, info.max
        ).astype(dtype_original)

    else:
        # PCM con signo, por ejemplo int16 o int32
        audio_guardar = np.clip(
            np.round(audio_filtrado * info.max),
            info.min, info.max
        ).astype(dtype_original)

else:
    # WAV de punto flotante
    audio_guardar = audio_filtrado.astype(dtype_original)

# Guardar con la frecuencia de muestreo original
wavfile.write("cancion_filtrada.wav", fs, audio_guardar)