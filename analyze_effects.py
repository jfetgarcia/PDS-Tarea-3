import numpy as np
from efectos_fir import eco, reverberacion


def calcular_snr(senal, ruido):
    senal = np.asarray(senal, dtype=np.float64)
    ruido = np.asarray(ruido, dtype=np.float64)

    potencia_senal = np.mean(senal**2)
    potencia_ruido = np.mean(ruido**2)

    if potencia_ruido == 0:
        return np.inf if potencia_senal > 0 else np.nan

    if potencia_senal == 0:
        return -np.inf

    snr = 10 * np.log10(potencia_senal / potencia_ruido)

    return snr

fs = 44100
f0 = 1000
duracion = 2

t = np.arange(int(fs * duracion)) / fs

# Tono puro de 1000 Hz
x = 0.5 * np.sin(2 * np.pi * f0 * t)

# Crear impulso unitario
impulso = np.array([1.0])

# Obtener respuestas al impulso
h_eco = eco(impulso, fs)
h_reverberacion = reverberacion(impulso, fs)

# Obtener respuesta al impulso equivalente
h_eq = reverberacion(eco(impulso, fs), fs)

tono_eco = eco(x, fs)
tono_reverberacion = reverberacion(tono_eco, fs)

tono_conv_eco = np.convolve(x, h_eco, mode="full")
tono_conv_reverberacion = np.convolve(tono_conv_eco, h_reverberacion, mode="full")

tono_conv_equivalente = np.convolve(x, h_eq, mode="full")

# Verificar dimensiones
assert tono_reverberacion.shape == tono_conv_reverberacion.shape

# Calcular error
ruido = tono_reverberacion - tono_conv_reverberacion

# Calcular SNR
snr = calcular_snr(tono_reverberacion, ruido)

# Calcular error máximo absoluto
error_maximo = np.max(np.abs(tono_reverberacion - tono_conv_reverberacion))

print(f"SNR cascada: {snr:.2f} dB")
print(f"Error máximo cascada: {error_maximo:.12e}")

# Verificar dimensiones
assert tono_reverberacion.shape == tono_conv_equivalente.shape

# Calcular error
ruido_eq = tono_reverberacion - tono_conv_equivalente

# Calcular SNR
snr_eq = calcular_snr(tono_reverberacion, ruido_eq)

# Calcular error máximo absoluto
error_maximo_eq = np.max(np.abs(tono_reverberacion - tono_conv_equivalente))

print(f"SNR sistema equivalente: {snr_eq:.2f} dB")
print(f"Error máximo sistema equivalente: {error_maximo_eq:.12e}")
