import cv2
import numpy as np
import sounddevice as sd
import mediapipe as mp
import threading
import time
import pygame

# === Load background images ===
# Ubah ukuran semua gambar background menjadi 640x480
IMG_SIZE = (640, 480)
img_idle = cv2.resize(cv2.imread('stadion.jpg'), IMG_SIZE)         # Gambar default ketika tidak ada input
img_cheer = cv2.resize(cv2.imread('teriak.jpg'), IMG_SIZE)         # Gambar saat pengguna bersuara keras
img_clap = cv2.resize(cv2.imread('tepuktangan.jpg'), IMG_SIZE)     # Gambar saat tangan terdeteksi

# === Shared state untuk komunikasi antar thread ===
status_lock = threading.Lock()     # Lock agar tidak terjadi konflik saat mengakses status bersama
audio_status = "idle"              # Status berdasarkan input suara (idle atau cheer)
gesture_status = "idle"            # Status berdasarkan gesture tangan (idle atau clap)
current_status = "idle"            # Status akhir yang menentukan background dan suara

# === Inisialisasi MediaPipe untuk segmentasi dan deteksi tangan ===
mp_selfie = mp.solutions.selfie_segmentation
segmentor = mp_selfie.SelfieSegmentation(model_selection=0)       # Model segmentasi untuk memisahkan orang dari latar belakang
mp_hands = mp.solutions.hands

# === Inisialisasi pygame untuk memainkan file audio ===
pygame.mixer.init()
sound_cheer = pygame.mixer.Sound('teriak.wav')                     # Suara sorakan
sound_clap = pygame.mixer.Sound('tepuktangan.wav')                # Suara tepuk tangan

# === Parameter untuk debounce suara ===
last_active_time = 0              # Waktu terakhir suara keras terdeteksi
debounce_time = 1.0               # Delay agar suara tidak langsung dianggap hilang

clap_sound_playing = False        # Status apakah suara tepuk tangan sedang dimainkan

# === Parameter untuk debounce deteksi tangan ===
last_hand_seen_time = 0
hand_timeout = 0.5                # Jika tidak ada tangan selama 0.5 detik, status gesture kembali ke idle

# === Fungsi untuk memperbarui status berdasarkan input suara ===
def update_status_audio(new_status):
    global audio_status
    with status_lock:
        if audio_status != new_status:
            print(f"[Audio Status] {audio_status} -> {new_status}")
            if new_status == "cheer":
                sound_clap.stop()                                # Hentikan tepuk tangan jika sedang main
                if audio_status != "cheer":
                    sound_cheer.play(loops=-1)                   # Mainkan suara teriak secara looping
            elif new_status == "idle":
                sound_cheer.stop()                               # Hentikan suara teriak
            audio_status = new_status
        else:
            # Pastikan suara tetap menyala kalau sudah cheer tapi tiba-tiba mati
            if new_status == "cheer" and not pygame.mixer.get_busy():
                sound_cheer.play(loops=-1)

# === Fungsi untuk memperbarui status berdasarkan gesture tangan ===
def update_status_gesture(new_status):
    global gesture_status, clap_sound_playing
    with status_lock:
        if gesture_status != new_status:
            print(f"[Gesture Status] {gesture_status} -> {new_status}")
            gesture_status = new_status

            if new_status == "clap":
                if not clap_sound_playing:
                    print("Play sound clap")
                    sound_cheer.stop()                           # Hentikan suara cheer jika sedang main
                    sound_clap.play(loops=-1)                    # Mainkan suara tepuk tangan
                    clap_sound_playing = True
                    time.sleep(0.1)                              # Delay untuk stabilitas
            else:
                if clap_sound_playing:
                    print("Stop sound clap")
                    sound_clap.stop()
                    clap_sound_playing = False
                    time.sleep(0.05)

# === Fungsi untuk menentukan status akhir berdasarkan input audio dan gesture ===
def compute_final_status():
    global current_status
    with status_lock:
        prev_status = current_status
        if gesture_status == "clap":
            current_status = "clap"                              # Gesture lebih prioritas
        elif audio_status == "cheer":
            current_status = "cheer"
        else:
            current_status = "idle"
        return prev_status != current_status                     # Return apakah status berubah

# === Fungsi callback untuk input suara real-time ===
def audio_callback(indata, frames, time_, status):
    global last_active_time
    if status:
        print(f"Audio status: {status}", flush=True)

    # Hitung volume suara dalam dB menggunakan RMS
    rms = np.sqrt(np.mean(indata**2))
    db = 20 * np.log10(rms + 1e-10)  # Tambahkan epsilon agar tidak log(0)
    now = time.time()
    print(f"Audio RMS dB: {db:.2f}", flush=True)

    threshold_db = -20              # Ambang batas suara
    if db > threshold_db:
        update_status_audio("cheer")
        last_active_time = now
    else:
        if now - last_active_time > debounce_time:
            update_status_audio("idle")

# === Thread untuk menangkap input suara terus-menerus ===
def audio_thread(device_index=None):
    kwargs = dict(channels=1, callback=audio_callback, samplerate=44100, blocksize=1024)
    if device_index is not None:
        kwargs['device'] = device_index
    try:
        with sd.InputStream(**kwargs):
            while True:
                time.sleep(0.1)
    except Exception as e:
        print(f"Audio stream error: {e}")

# === Fungsi untuk mengganti background menggunakan segmentasi MediaPipe ===
def apply_virtual_background(frame, bg_image):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = segmentor.process(rgb)

    if result.segmentation_mask is None:
        return frame

    mask = result.segmentation_mask
    mask_fg = mask > 0.5                                             # Deteksi area manusia

    bg_resized = cv2.resize(bg_image, (frame.shape[1], frame.shape[0]))
    mask_fg_3c = np.repeat(mask_fg[:, :, np.newaxis], 3, axis=2)    # Buat mask jadi 3 channel

    fg = frame * mask_fg_3c                                          # Ambil bagian manusia dari frame
    bg = bg_resized * (~mask_fg_3c)                                  # Ambil bagian background dari gambar

    output = fg + bg                                                 # Gabungkan keduanya
    return output.astype(np.uint8)

# === Fungsi utama loop tampilan webcam dan gesture ===
def display_loop():
    global current_status, last_hand_seen_time

    hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_SIZE[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_SIZE[1])

    if not cap.isOpened():
        print("❌ Kamera tidak tersedia.")
        return

    cv2.namedWindow("Filter Stadion", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Filter Stadion", *IMG_SIZE)

    last_hand_seen_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, IMG_SIZE)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        now = time.time()

        # Jika tangan terdeteksi
        if results.multi_hand_landmarks:
            tangan_terdeteksi = len(results.multi_hand_landmarks)
            last_hand_seen_time = now
            update_status_gesture("clap")
        else:
            # Jika tidak terlihat tangan terlalu lama, reset gesture
            if now - last_hand_seen_time > hand_timeout:
                update_status_gesture("idle")
            else:
                update_status_gesture("clap")

        _ = compute_final_status()

        # Tentukan background berdasarkan status akhir
        with status_lock:
            if current_status == "cheer":
                bg = img_cheer
            elif current_status == "clap":
                bg = img_clap
            else:
                bg = img_idle

        # Terapkan virtual background
        frame_out = apply_virtual_background(frame, bg)
        cv2.imshow("Filter Stadion", frame_out)

        # Tekan 'q' untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# === Program utama ===
if __name__ == "__main__":
    print("Daftar device audio yang tersedia:")
    print(sd.query_devices())                                       # Menampilkan daftar perangkat audio

    device_index = None                                             # Ganti jika perlu memilih mikrofon spesifik

    # Mulai thread audio dan tampilan webcam
    threading.Thread(target=audio_thread, args=(device_index,), daemon=True).start()
    display_loop()
