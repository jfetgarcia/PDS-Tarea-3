import matplotlib.pyplot as plt
import numpy as np
from sonar_channel import sonar_channel

def main():
    # Frecuencias Hz
    fi = 20000
    ff = 30000
    fs = 96000

    # T de chirp en s
    T = 0.010
    tiempo = np.arange(0,T,1/fs)

    # velocidad (m/s) aprox. de sonido en agua marina
    vel_agua = 1500 

    f_chirp = (fi*tiempo + ((ff-fi)/(2*T))*tiempo**2)
    x = np.cos(2*np.pi*f_chirp)

    # Graficar
    plt.figure(figsize=(12, 4))
    plt.plot(tiempo * 1000, x)

    #plt.title("Señal Chirp (20 kHz - 30 kHz)")
    #plt.xlabel("Tiempo (ms)")
    #plt.ylabel("Amplitud")
    #plt.grid(True)
    #plt.xlim(0, T * 1000)
    #plt.show()

    recibido = sonar_channel(x,fs)
    correlacion = np.correlate(recibido,x, mode="full")

    # Posibles desplazamientos de la senal
    desplazamientos = np.arange(-(len(x) - 1), len(recibido))

    # Buscando atraso
    n0 = desplazamientos[np.argmax(correlacion)]
    tau_prop = n0/fs
    distancia = (vel_agua*tau_prop)/2

    print(f"Atraso estimado: {n0} muestras")
    print(f"Atraso temporal: {tau_prop * 1000:.4f} ms")
    print(f"Distancia estimada: {distancia:.4f} m")

    plt.xlabel("Desplazamiento (muestras)")
    plt.ylabel("Correlación cruzada")
    plt.title("Correlación cruzada entre x[n] y y[n]")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()