# TBO-Modular-NFA-DFA-Converter

Aplikasi modular simulasi **Deterministic Finite Automata (DFA)**, **Non-Deterministic Finite Automata (NFA)**, serta konversi otomatis NFA ke DFA menggunakan algoritma **Subset Construction (Powerset Construction)** secara mandiri berbasis Python murni (*zero external automata dependencies*).

Tugas Proyek Ujian Tengah Semester (UTS) Mata Kuliah **Teori Bahasa dan Otomata (TBO)**.

---

## 👤 Identitas Pengembang
* **Nama** : Andi Rasyihan Jawahir
* **NIM** : 105841111524
* **Kelas** : 5F (Informatika)
* **Program Studi** : Informatika, Fakultas Teknik
* **Perguruan Tinggi** : Universitas Muhammadiyah Makassar
* **Dosen Pengampu** : Chyquitha Danuputri, S.Kom., M.Kom.

---

## 🏛️ Arsitektur Sistem Modular
Sistem dibangun menerapkan prinsip *High Cohesion & Low Coupling*, dipecah menjadi modul-modul terpisah:

| Nama Modul | Fungsi Utama |
| :--- | :--- |
| **`dfa_simulator.py`** | Kelas `DFA` (5-tupel: $Q, \Sigma, \delta, q_0, F$), validasi determinisme, dan penelusuran string (*tracing*) langkah demi langkah. |
| **`nfa_simulator.py`** | Kelas `NFA`, penanganan *multi-state tracking*, $\epsilon$-move, serta fungsi rekursif komputasi $\epsilon$-closure. |
| **`subset_converter.py`** | Algoritma `subset_construction(nfa)` yang secara matematis memetakan subset state NFA menjadi state DFA ($A, B, C, \dots$), menangani *dead state*, dan menetapkan final state. |
| **`visualizer.py`** | Pembangkitan visualisasi diagram alir arsitektur sistem, flowchart algoritma subset construction, dan diagram state automata berbasis Matplotlib. |
| **`main.py`** | Pengendali utama (*Controller*) yang menyajikan antarmuka CLI (*Command Line Interface*) interaktif 6 menu navigasi dan automated test suite (`--auto-test`). |

---

## 🚀 Fitur Unggulan
1. **Representasi Formal 5-Tupel Murni:** Dibangun menggunakan struktur data bawaan Python (`dict`, `set`, `frozenset`, `tuple`).
2. **Simulasi Tracing Lengkap:** Menampilkan tabel transisi langkah demi langkah untuk setiap simbol masukan.
3. **Konversi Otomatis NFA ke DFA:** Mengimplementasikan Subset Construction lengkap dengan penamaan relabeling state ($A, B, C, \dots$).
4. **Pembuktian Ekuivalensi Bahasa:** Verifikasi konsistensi keputusan antara NFA asli dan DFA hasil konversi (100% Identik/Valid).
5. **Preset Materi Kuliah & Mode Kustom:** Menyediakan contoh automata materi perkuliahan serta mode interaktif untuk memasukkan NFA buatan sendiri.

---

## 💻 Cara Menjalankan Program

### Prasyarat
* Python 3.8 atau lebih baru.
* Pustaka visualisasi (opsional untuk menu visual):
  ```bash
  pip install matplotlib
  ```

### Menjalankan Mode Interaktif (CLI)
```bash
python main.py
```

### Menjalankan Automated Test Suite
```bash
python main.py --auto-test
```

---

## 📜 Lisensi
Dikembangkan untuk keperluan akademik tugas perkuliahan Teori Bahasa dan Otomata (TBO), Program Studi Informatika, Universitas Muhammadiyah Makassar.
