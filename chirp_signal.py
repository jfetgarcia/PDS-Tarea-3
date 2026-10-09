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

    # Grafica chirp
    plt.figure(figsize=(12, 4))
    plt.plot(tiempo * 1000, x)

    plt.title("Señal Chirp (20 kHz - 30 kHz)")
    plt.xlabel("Tiempo (ms)")
    plt.ylabel("Amplitud")
    plt.grid(True)
    plt.xlim(0, T * 1000)

    recibido = sonar_channel(x,fs)
    correlacion = np.correlate(recibido,x, mode="full")

    # Posibles desplazamientos de la senal
    desplazamientos = np.arange(-(len(x) - 1), len(recibido))

    # Buscando atraso
    n0 = desplazamientos[np.argmax(correlacion)]
    tau_prop = n0/fs
    distancia = (vel_agua*tau_prop)/2

    # Resolucion espacial
    B = ff -fi
    res_espacial = vel_agua / (2*B)

    # Duracion min/max de chirp
    # Niveles en (dB)
    sl = 190
    di = 10
    ts = -5
    nl0 = 69.2
    # en dB/km
    alpha = 6

    tiempo_pruebas = np.arange(1e-3,1,1/fs)

    tl = (20*np.log10(distancia))+(alpha*distancia/1000)
    nl = nl0 + (10*np.log10(B))
    pg = 10*np.log10(B*tiempo_pruebas)

    snr = sl-(2*tl)+ts-nl+di+pg

    print(f"Atraso estimado: {n0} muestras")
    print(f"Atraso temporal: {tau_prop * 1000} ms")
    print(f"Distancia estimada: {distancia} m")
    print(f"Resolucion espacial: {res_espacial} m")

    # Grafica correlacion
    plt.figure(figsize=(10, 4))
    plt.plot(desplazamientos, correlacion)

    plt.axvline(n0, color="red", linestyle="--",
            label=f"Atraso = {n0} muestras")
    plt.xlabel("Desplazamiento (muestras)")
    plt.ylabel("Correlación cruzada")
    plt.title("Correlación cruzada entre x[n] y y[n]")
    plt.legend()
    plt.grid(True)

    # Grafica duraciones max/min de chirp
    # Línea horizontal en 10 dB
    # Umbral de SNR
    umbral = 10

    # Encontrar el primer valor que supera 10 dB
    indices = np.where(snr > umbral)[0]

    plt.figure(figsize=(12, 5))

    plt.plot(tiempo_pruebas * 1000, snr, label="SNR")
    plt.axhline(y=umbral, color="red", linestyle="--",
                label="Umbral SNR = 10 dB")

    if len(indices) > 0:
        idx = indices[0]

        tiempo_umbral = tiempo_pruebas[idx] * 1000
        snr_umbral = snr[idx]

        # Marcar el primer punto que supera 10 dB
        plt.scatter(tiempo_umbral, snr_umbral,
                    color="green", s=80, zorder=5)

        # Línea vertical en el tiempo correspondiente
        plt.axvline(x=tiempo_umbral, color="green",
                    linestyle="--", alpha=0.7)

        plt.annotate(
            f"{tiempo_umbral:.2f} ms",
            (tiempo_umbral, snr_umbral),
            xytext=(10, 15),
            textcoords="offset points"
        )

        print(f"SNR supera 10 dB a partir de {tiempo_umbral} ms")
    else:
        print("El SNR no supera los 10 dB en el intervalo analizado.")

    plt.xlabel("Duración del chirp (ms)")
    plt.ylabel("SNR (dB)")
    plt.title("SNR en función de la duración del chirp")
    plt.grid(True)
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main()