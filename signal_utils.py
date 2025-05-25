import numpy as np # Mengimpor NumPy untuk operasi numerik dan array
from scipy.signal import butter, filtfilt # Mengimpor fungsi filter Butterworth dan filtfilt dari SciPy

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    """
    Menerapkan filter bandpass Butterworth ke data sinyal.

    Filter ini melewatkan frekuensi dalam rentang tertentu (antara lowcut dan highcut)
    dan meredam frekuensi di luar rentang tersebut. Menggunakan filtfilt untuk
    pemfilteran zero-phase.

    Args:
        data (numpy.ndarray atau list): Sinyal input 1D.
        lowcut (float): Frekuensi cut-off bawah (Hz).
        highcut (float): Frekuensi cut-off atas (Hz).
        fs (float): Frekuensi sampling sinyal (Hz).
        order (int, optional): Orde filter Butterworth. Defaultnya adalah 5.

    Returns:
        numpy.ndarray: Sinyal yang telah difilter.
    """
    nyq = 0.5 * fs  # Menghitung frekuensi Nyquist (setengah dari frekuensi sampling)
    low = lowcut / nyq  # Normalisasi frekuensi cut-off bawah terhadap frekuensi Nyquist
    high = highcut / nyq  # Normalisasi frekuensi cut-off atas terhadap frekuensi Nyquist
    
    # Mendesain koefisien filter Butterworth (numerator b, denominator a)
    # 'band' menunjukkan tipe filter adalah bandpass
    b, a = butter(order, [low, high], btype='band') #
    
    # Menerapkan filter ke data menggunakan filtfilt
    # filtfilt menerapkan filter dua kali (sekali maju, sekali mundur) untuk menghasilkan output zero-phase
    # (tidak ada pergeseran fasa yang disebabkan oleh filter).
    y = filtfilt(b, a, data) #
    return y

def normalize_signal(signal):
    """
    Menormalisasi sinyal ke rentang [0, 1].

    Normalisasi dilakukan dengan mengurangkan nilai minimum sinyal dan kemudian
    membaginya dengan rentang (nilai maksimum dikurangi nilai minimum).

    Args:
        signal (numpy.ndarray atau list): Sinyal input.

    Returns:
        numpy.ndarray: Sinyal yang telah dinormalisasi. Jika sinyal input konstan,
                       akan mengembalikan array berisi nol.
    """
    signal = np.array(signal) # Konversi input ke NumPy array untuk operasi vektor
    min_val = np.min(signal) # Cari nilai minimum dalam sinyal
    max_val = np.max(signal) # Cari nilai maksimum dalam sinyal
    
    # Hindari pembagian dengan nol jika sinyal konstan (max_val == min_val)
    if max_val == min_val:
        return np.zeros_like(signal) # Kembalikan array nol jika sinyal flat
        
    # Rumus normalisasi min-max
    return (signal - min_val) / (max_val - min_val) #

def smooth_signal(signal, window_len=5):
    """
    Menghaluskan sinyal menggunakan filter moving average sederhana.

    Setiap titik pada sinyal output adalah rata-rata dari sejumlah titik tetangga
    (ditentukan oleh window_len) pada sinyal input.

    Args:
        signal (numpy.ndarray atau list): Sinyal input.
        window_len (int, optional): Panjang jendela moving average. Harus ganjil
                                    agar hasilnya simetris. Defaultnya adalah 5.

    Returns:
        numpy.ndarray: Sinyal yang telah dihaluskan.
    """
    # Pastikan window_len adalah ganjil untuk hasil yang lebih baik pada mode 'same'
    if window_len % 2 == 0:
        window_len += 1 # Jika genap, tambahkan 1 agar menjadi ganjil
        
    # Membuat jendela filter (kernel) dengan bobot yang sama
    window = np.ones(window_len) / window_len #
    
    # Melakukan konvolusi antara sinyal dan jendela filter
    # mode='same' menghasilkan output dengan panjang yang sama dengan input,
    # dengan penanganan padding yang sesuai di tepi sinyal.
    return np.convolve(signal, window, mode='same') #