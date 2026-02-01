import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image

# --- KONFIGURASI ---
IMG_SIZE = (224, 224) # Sesuaikan dengan input shape model Anda
MODEL_PATH = "best_model.h5" # Pastikan nama file sesuai

# Definisi Kelas (Sesuai urutan training model Anda)
class_names = [
    'Abrasions', 'Bruises', 'Burns', 'Cut', 'Diabetic Wounds', 
    'Laceration', 'Normal', 'Pressure Wounds', 'Surgical Wounds', 'Venous Wounds'
]

# Mapping Bahasa Inggris -> Indonesia untuk UI
translation_map = {
    'Abrasions': 'Luka Lecet (Abrasi)',
    'Bruises': 'Memar',
    'Burns': 'Luka Bakar',
    'Cut': 'Luka Sayat',
    'Diabetic Wounds': 'Luka Diabetes',
    'Laceration': 'Luka Robek',
    'Normal': 'Normal/Sehat',
    'Pressure Wounds': 'Luka Tekan (Dekubitus)',
    'Surgical Wounds': 'Luka Operasi',
    'Venous Wounds': 'Luka Vena'
}

# --- LOAD MODEL ---
try:
    best_model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model berhasil dimuat.")
except Exception as e:
    best_model = None
    print(f"❌ Error memuat model: {e}")

# --- LOGIKA REKOMENDASI ---
def get_first_aid_recommendation(wound_class):
    rekomendasi = {
        'Abrasions': (
            "1. Bersihkan luka dengan air mengalir untuk membuang kotoran.\n"
            "2. Gunakan sabun lembut di sekitar luka (jangan terkena luka langsung).\n"
            "3. Oleskan salep antibiotik atau petroleum jelly untuk menjaga kelembapan.\n"
            "4. Tutup dengan plester bersih jika luka berada di area yang mudah tergesek."
        ),
        'Bruises': (
            "1. Istirahatkan area yang memar.\n"
            "2. Kompres dingin selama 15-20 menit untuk mengurangi pembengkakan.\n"
            "3. Posisikan bagian tubuh yang memar lebih tinggi dari jantung.\n"
            "4. Gunakan obat pereda nyeri jika diperlukan."
        ),
        'Burns': (
            "1. Alirkan air biasa (bukan air es) pada area luka selama 10-20 menit.\n"
            "2. Lepaskan perhiasan atau pakaian yang ketat sebelum area membengkak.\n"
            "3. Tutup longgar dengan kain bersih atau kasa steril.\n"
            "4. **Jangan** memecahkan lepuh yang muncul."
        ),
        'Cut': (
            "1. Tekan luka kuat-kuat dengan kain bersih selama 5-10 menit hingga darah berhenti.\n"
            "2. Bersihkan luka dengan air mengalir.\n"
            "3. Oleskan antiseptik pada pinggiran luka.\n"
            "4. Rekatkan plester atau perban steril."
        ),
        'Diabetic Wounds': (
            "**Peringatan:** Luka diabetes membutuhkan perhatian khusus.\n"
            "1. Cuci luka dengan cairan saline (NaCl 0.9%).\n"
            "2. Jaga luka tetap kering dan tutup dengan kasa steril.\n"
            "3. Periksa tanda-tanda infeksi seperti nanah atau bau.\n"
            "4. Segera hubungi dokter spesialis luka."
        ),
        'Laceration': (
            "1. Hentikan perdarahan dengan menekan luka secara stabil.\n"
            "2. Jika luka dalam dan robekannya lebar, segera tutup dengan kasa.\n"
            "3. Jangan mencoba mencuci luka jika perdarahan sangat deras.\n"
            "4. **Segera ke IGD** karena mungkin memerlukan jahitan medis."
        ),
        'Normal': "Kulit terlihat normal dan sehat. Tetap jaga kebersihan area tersebut.",
        'Pressure Wounds': (
            "1. Hilangkan tekanan pada area luka dengan mengubah posisi tubuh.\n"
            "2. Gunakan bantal atau bantalan pelindung khusus.\n"
            "3. Bersihkan area secara lembut dengan cairan saline.\n"
            "4. Jaga kulit di sekitarnya tetap lembap."
        ),
        'Surgical Wounds': (
            "1. Ikuti instruksi penggantian perban dari dokter bedah Anda.\n"
            "2. Jangan menggaruk area jahitan.\n"
            "3. Jaga agar luka tetap kering saat mandi (gunakan penutup tahan air).\n"
            "4. Lapor dokter jika jahitan terbuka atau muncul kemerahan hebat."
        ),
        'Venous Wounds': (
            "1. Gunakan stoking kompresi jika disarankan oleh medis.\n"
            "2. Angkat kaki lebih tinggi dari jantung saat berbaring.\n"
            "3. Lakukan aktivitas fisik ringan secara teratur.\n"
            "4. Jaga kelembapan kulit di sekitar luka."
        )
    }
    return rekomendasi.get(wound_class, "Rekomendasi belum tersedia. Silakan konsultasi dengan petugas medis.")

# --- FUNGSI PREDIKSI ---
def predict_image(image_input):
    if best_model is None:
        return {}, "⚠️ Model tidak ditemukan. Harap upload file model (.h5)."

    if image_input is None:
        return {}, "Silakan upload gambar."

    # Preprocessing
    img = image_input.resize(IMG_SIZE)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    img_array = img_array / 255.0

    # Prediksi
    predictions = best_model.predict(img_array)
    scores = tf.nn.softmax(predictions[0]).numpy()

    # Mapping hasil untuk UI (Bahasa Indonesia)
    translated_output_dict = {
        translation_map.get(class_names[i], class_names[i]): float(scores[i])
        for i in range(len(class_names))
    }

    # Ambil label tertinggi
    top_idx = np.argmax(scores)
    top_label_en = class_names[top_idx]
    top_confidence = scores[top_idx]

    # --- LOGIKA THRESHOLD ---
    THRESHOLD = 0.50

    if top_confidence < THRESHOLD:
        top_label_id = "Normal (Tidak Terdeteksi)"
        rekomendasi_teks = (
            "**Mohon Maaf:** Model kurang akurat dalam menganalisis foto ini.\n\n"
            "**Saran:**\n"
            "1. Pastikan area luka terlihat jelas dan tidak blur.\n"
            "2. Gunakan pencahayaan yang cukup (terang).\n"
            "3. Ambil foto dari sudut tegak lurus ke arah luka.\n\n"
            "Jika Anda merasa luka ini serius, segera hubungi tenaga medis meskipun hasil analisis tidak muncul."
        )
    else:
        top_label_id = translation_map.get(top_label_en, top_label_en)
        rekomendasi_teks = get_first_aid_recommendation(top_label_en)

    # Format Markdown untuk Gradio
    formatted_output = (
        f"### Analisis: **{top_label_id}**\n\n"
        f"**Langkah Pertolongan:**\n{rekomendasi_teks}\n\n"
        f"--- \n*Tingkat Keyakinan AI: {top_confidence:.2%}*"
    )

    return translated_output_dict, formatted_output

# --- UI INTERFACE ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="red", secondary_hue="slate")) as demo:
    gr.Markdown("# 🚨 FirstAidLens")
    gr.Markdown("Deteksi jenis luka secara instan dan dapatkan panduan pertolongan pertama yang tepat.")

    with gr.Row():
        with gr.Column(scale=1):
            input_img = gr.Image(
                sources=["upload", "webcam"],
                type="pil",
                label="Ambil Foto Luka"
            )
            gr.Markdown("> **Penting:** Hasil AI ini hanya referensi awal. Jika luka parah atau pendarahan tidak berhenti, segera hubungi **112**.")

        with gr.Column(scale=1):
            output_label = gr.Label(num_top_classes=3, label="Hasil Analisis Jenis Luka")
            output_markdown = gr.Markdown("### Panduan Pertolongan Pertama\n_Upload atau ambil foto untuk melihat rekomendasi._")

    # Trigger otomatis saat gambar diupload/diambil
    input_img.change(
        fn=predict_image,
        inputs=input_img,
        outputs=[output_label, output_markdown]
    )

# Launch (Server Name 0.0.0.0 wajib untuk Docker)
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)