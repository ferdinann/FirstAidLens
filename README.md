# 🚨 FirstAidLens

**FirstAidLens** adalah asisten medis berbasis AI yang mampu mengidentifikasi jenis luka melalui foto dan memberikan panduan pertolongan pertama (*First Aid*) yang relevan secara medis. Aplikasi ini bertujuan untuk memberikan respons cepat bagi masyarakat awam sebelum bantuan medis profesional tiba.

---

## 📋 Fitur Utama
* **Identifikasi 10 Jenis Luka:** Termasuk Abrasions (Lecet), Burns (Luka Bakar), Laceration (Robek), hingga Diabetic Wounds.
* **Smart Thresholding:** Jika keyakinan AI di bawah 20%, sistem akan meminta pengambilan foto ulang demi keamanan.
* **Panduan Langkah-demi-Langkah:** Instruksi penanganan luka yang terstruktur dan mudah dipahami.
* **Dukungan Bahasa Indonesia:** Seluruh antarmuka dan rekomendasi disajikan dalam Bahasa Indonesia.

## 🛠️ Teknologi yang Digunakan
* **Framework:** TensorFlow / Keras
* **UI/UX:** Gradio (Blocks API)
* **Image Processing:** PIL (Pillow), NumPy
* **Model Base:** Convolutional Neural Network (CNN)
