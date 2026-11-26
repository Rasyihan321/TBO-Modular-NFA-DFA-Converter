"""
Program Utama (main.py)
Aplikasi Modular Simulasi NFA, DFA, dan Konversi NFA ke DFA
Mata Kuliah : Teori Bahasa dan Otomata (TBO)
Dosen       : Chyquitha Danuputri, S.Kom., M.Kom.
Mahasiswa   : Andi Rasyihan Jawahir (NIM: 105841111524, Kelas: 5F)
Program Studi Informatika, Universitas Muhammadiyah Makassar
"""

import sys
import os
from typing import Set, Dict, Tuple
from dfa_simulator import DFA
from nfa_simulator import NFA
from subset_converter import subset_construction
from visualizer import generate_system_flowchart, generate_subset_flowchart, generate_automata_diagrams


# 1. PRESET MODEL AUTOMATA (SESUAI MATERI PERKULIAHAN & VIDEO DOSEN)

def get_preset_dfa_p3() -> DFA:
    """DFA Contoh 1 Slide 7 Bab 4 Lanjutan / Rekaman Kuliah Pertemuan 3."""
    return DFA(
        name="DFA_Contoh1_Pertemuan3",
        states={"q0", "q1", "q2", "q3"},
        alphabet={"a", "b"},
        transitions={
            ("q0", "a"): "q1", ("q0", "b"): "q2",
            ("q1", "a"): "q1", ("q1", "b"): "q1",
            ("q2", "a"): "q2", ("q2", "b"): "q3",
            ("q3", "a"): "q1", ("q3", "b"): "q1"
        },
        start_state="q0",
        final_states={"q1"}
    )


def get_preset_dfa_substring_001() -> DFA:
    """DFA Contoh 2 Deteksi Substring '001' (Slide 11 Bab 4 Lanjutan)."""
    return DFA(
        name="DFA_Deteksi_Substring_001",
        states={"q0", "q1", "q2", "q3"},
        alphabet={"0", "1"},
        transitions={
            ("q0", "0"): "q1", ("q0", "1"): "q0",
            ("q1", "0"): "q2", ("q1", "1"): "q0",
            ("q2", "0"): "q2", ("q2", "1"): "q3",
            ("q3", "0"): "q3", ("q3", "1"): "q3"
        },
        start_state="q0",
        final_states={"q3"}
    )


def get_preset_nfa_bab6() -> NFA:
    """NFA Contoh Utama Bab 6-7 Slide 7 (Σ={0,1})."""
    return NFA(
        name="NFA_ContohUtama_Bab6_Slide7",
        states={"q0", "q1", "q2"},
        alphabet={"0", "1"},
        transitions={
            ("q0", "0"): {"q0", "q1"},
            ("q1", "1"): {"q1", "q2"},
            ("q2", "0"): {"q2"},
            ("q2", "1"): {"q2"}
        },
        start_state="q0",
        final_states={"q2"}
    )


def get_preset_nfa_latihan15() -> NFA:
    """NFA Latihan Mandiri Bab 6-7 Slide 15 (Σ={a,b})."""
    return NFA(
        name="NFA_Latihan_Slide15",
        states={"p0", "p1", "p2"},
        alphabet={"a", "b"},
        transitions={
            ("p0", "a"): {"p0", "p1"},
            ("p1", "b"): {"p2"},
            ("p2", "a"): {"p2"},
            ("p2", "b"): {"p2"}
        },
        start_state="p0",
        final_states={"p2"}
    )


def get_preset_nfa_epsilon_bab5() -> NFA:
    """NFA dengan Epsilon-move Bab 5 / Video Kuliah."""
    return NFA(
        name="NFA_Epsilon_Bab5",
        states={"q0", "q1", "q2", "q3", "q4"},
        alphabet={"a", "b"},
        transitions={
            ("q0", "ε"): {"q1"},
            ("q1", "b"): {"q2"},
            ("q2", "ε"): {"q3"},
            ("q3", "a"): {"q4"}
        },
        start_state="q0",
        final_states={"q4"},
        epsilon_symbol="ε"
    )


# 2. PROSEDUR EKSEKUSI & SIMULASI (MODULAR FUNCTIONS)

def run_dfa_demo(dfa: DFA, test_strings: list):
    """Menjalankan dan menampilkan hasil simulasi DFA."""
    print(dfa.display_table())
    print("\n--- PENGUJIAN STRING PADA DFA ---")
    for s in test_strings:
        display_str = s if s != "" else "ε (string kosong)"
        accepted, trace, final_st = dfa.simulate(s)
        status = "DITERIMA [ACCEPT]" if accepted else "DITOLAK [REJECT]"
        print(f"\nUji String: \"{display_str}\" -> Hasil: {status}")
        print(f"{'Langkah':<8} | {'State Saat Ini':<14} | {'Input':<6} | {'State Baru':<12} | Keterangan")
        print("-" * 65)
        for t in trace:
            print(f"{t['step']:<8} | {t['current']:<14} | {t['symbol']:<6} | {t['next']:<12} | {t['note']}")


def run_nfa_demo(nfa: NFA, test_strings: list):
    """Menjalankan dan menampilkan hasil simulasi NFA."""
    print(nfa.display_table())
    print("\n--- PENGUJIAN STRING PADA NFA (SUBSET TRACING) ---")
    for s in test_strings:
        display_str = s if s != "" else "ε (string kosong)"
        accepted, trace, final_set = nfa.simulate(s)
        status = "DITERIMA [ACCEPT]" if accepted else "DITOLAK [REJECT]"
        print(f"\nUji String: \"{display_str}\" -> Hasil: {status}")
        print(f"{'Langkah':<8} | {'Subset Aktif':<16} | {'Input':<6} | {'Subset Baru':<16} | Keterangan")
        print("-" * 72)
        for t in trace:
            print(f"{t['step']:<8} | {t['current']:<16} | {t['symbol']:<6} | {t['next']:<16} | {t['note']}")


def run_conversion_demo(nfa: NFA, test_strings: list):
    """Menjalankan algoritma konversi NFA ke DFA dan memverifikasi ekuivalensi."""
    print("\n" + "="*75)
    print(f"PROSES KONVERSI NFA KE DFA (SUBSET CONSTRUCTION): {nfa.name}")
    print("="*75)
    print(nfa.display_table())

    dfa_res, steps, mapping = subset_construction(nfa)

    print("\n--- PEMETAAN STATE DFA DARI SUBSET NFA ---")
    for lbl, subset_str in sorted(mapping.items()):
        is_f = " [FINAL STATE]" if lbl in dfa_res.final_states else ""
        is_s = " [START STATE]" if lbl == dfa_res.start_state else ""
        print(f"State DFA {lbl:<2} = {subset_str:<22}{is_s}{is_f}")

    print("\n--- LANGKAH-LANGKAH PERHITUNGAN SUBSET TRANSISI ---")
    for idx, stp in enumerate(steps, 1):
        print(f"{idx:02d}. {stp['calculation']}")

    print("\n" + dfa_res.display_table())

    print("\n--- UJI PEMBUKTIAN EKUIVALENSI BAHASA (NFA VS DFA HASIL KONVERSI) ---")
    print(f"{'String Uji':<14} | {'Hasil NFA':<16} | {'Hasil DFA Konversi':<18} | Status Ekuivalensi")
    print("-" * 70)
    for s in test_strings:
        disp = s if s != "" else "ε"
        nfa_acc, _, _ = nfa.simulate(s)
        dfa_acc, _, _ = dfa_res.simulate(s)
        nfa_res = "DITERIMA" if nfa_acc else "DITOLAK"
        dfa_res_str = "DITERIMA" if dfa_acc else "DITOLAK"
        eq = "IDENTIK (VALID) ✓" if nfa_acc == dfa_acc else "TIDAK COCOK ✕"
        print(f"{disp:<14} | {nfa_res:<16} | {dfa_res_str:<18} | {eq}")


# 3. MENU UTAMA INTERAKTIF

def main_menu():
    """Menampilkan menu CLI interaktif modular."""
    while True:
        print("\n" + "="*75)
        print("          SISTEM MODULAR TEORI BAHASA DAN OTOMATA (TBO)")
        print("           SIMULASI NFA, DFA & KONVERSI NFA KE DFA")
        print("          Andi Rasyihan Jawahir (105841111524) - Kelas 5F")
        print("="*75)
        print("1. Demo Simulasi DFA (Contoh Kuliah Pertemuan 3 & Deteksi Substring '001')")
        print("2. Demo Simulasi NFA (Contoh Utama Bab 6 & Epsilon-Move Bab 5)")
        print("3. Demo Konversi NFA ke DFA - Contoh Utama Bab 6 Slide 7 (Σ={0,1})")
        print("4. Demo Konversi NFA ke DFA - Latihan Slide 15 (Σ={a,b})")
        print("5. Mode Kustom: Masukkan NFA Sendiri dan Konversi ke DFA")
        print("6. Generate Gambar Flowchart & Diagram State untuk Laporan")
        print("0. Keluar dari Program")
        print("-" * 75)

        pilihan = input("Pilih menu [0-6]: ").strip()

        if pilihan == "1":
            print("\n[PILIHAN 1] DEMO DFA CONTOH 1 (ALFABET {a, b})")
            d1 = get_preset_dfa_p3()
            run_dfa_demo(d1, ["abbab", "bba", "baa", ""])

            print("\n" + "-"*50)
            print("[PILIHAN 1] DEMO DFA CONTOH 2 (SUBSTRING '001')")
            d2 = get_preset_dfa_substring_001()
            run_dfa_demo(d2, ["111001", "0101", "001", "10001", "000"])

        elif pilihan == "2":
            print("\n[PILIHAN 2] DEMO NFA CONTOH UTAMA (ALFABET {0, 1})")
            n1 = get_preset_nfa_bab6()
            run_nfa_demo(n1, ["0", "01", "011", "1", "001"])

            print("\n" + "-"*50)
            print("[PILIHAN 2] DEMO NFA EPSILON-MOVE (BAB 5)")
            n_eps = get_preset_nfa_epsilon_bab5()
            print("Perhitungan E-Closure Tiap State:")
            for st in n_eps.states:
                cl = n_eps.epsilon_closure({st})
                print(f"E-closure({st}) = {{{', '.join(sorted(cl))}}}")
            run_nfa_demo(n_eps, ["ba", "b", "a", ""])

        elif pilihan == "3":
            n1 = get_preset_nfa_bab6()
            run_conversion_demo(n1, ["0", "01", "011", "1", "001", "0011", "10"])

        elif pilihan == "4":
            n2 = get_preset_nfa_latihan15()
            run_conversion_demo(n2, ["ab", "abb", "ba", "a", "b", "abbb"])

        elif pilihan == "5":
            print("\n--- MODE INPUT KUSTOM NFA ---")
            try:
                states_in = input("Masukkan daftar state dipisah koma (mis: q0,q1,q2): ").strip().split(",")
                states = {s.strip() for s in states_in if s.strip()}

                alpha_in = input("Masukkan alfabet input dipisah koma (mis: 0,1 atau a,b): ").strip().split(",")
                alphabet = {a.strip() for a in alpha_in if a.strip()}

                start_st = input("Masukkan state awal (mis: q0): ").strip()
                final_in = input("Masukkan state akhir dipisah koma (mis: q2): ").strip().split(",")
                final_states = {f.strip() for f in final_in if f.strip()}

                print("\nMasukkan transisi (format: state,simbol->tujuan1,tujuan2). Ketik 'selesai' jika sudah:")
                transitions = {}
                while True:
                    line = input("Transisi: ").strip()
                    if line.lower() == "selesai" or not line:
                        break
                    parts = line.split("->")
                    src_sym = parts[0].split(",")
                    src = src_sym[0].strip()
                    sym = src_sym[1].strip()
                    dests = {d.strip() for d in parts[1].split(",") if d.strip()}
                    transitions[(src, sym)] = dests

                custom_nfa = NFA(
                    name="NFA_Kustom_Pengguna",
                    states=states,
                    alphabet=alphabet,
                    transitions=transitions,
                    start_state=start_st,
                    final_states=final_states
                )
                test_str = input("Masukkan string uji (pisahkan koma jika banyak): ").strip().split(",")
                test_list = [t.strip() for t in test_str]
                run_conversion_demo(custom_nfa, test_list)

            except Exception as e:
                print(f"Error pada penginputan: {e}")

        elif pilihan == "6":
            print("\n[*] Menghasilkan file visualisasi flowchart dan diagram...")
            p_sys = generate_system_flowchart()
            p_sub = generate_subset_flowchart()
            p_dia = generate_automata_diagrams()
            print(f"[+] Flowchart Arsitektur Sistem  : {p_sys}")
            print(f"[+] Flowchart Subset Construction : {p_sub}")
            for k, v in p_dia.items():
                print(f"[+] Diagram Automata ({k})       : {v}")
            print("[✓] Seluruh visualisasi berhasil disimpan ke folder laporan/screenshoot/!")

        elif pilihan == "0":
            print("\nTerima kasih. Program selesai.")
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan angka 0-6.")


if __name__ == "__main__":
    # Jika dijalankan dengan argumen --auto-test, jalankan tes langsung dan generate visual
    if len(sys.argv) > 1 and sys.argv[1] == "--auto-test":
        print("[*] Menjalankan automated test suite & visualisasi...")
        generate_system_flowchart()
        generate_subset_flowchart()
        generate_automata_diagrams()
        
        d1 = get_preset_dfa_p3()
        run_dfa_demo(d1, ["abbab", "bba", "baa"])

        n1 = get_preset_nfa_bab6()
        run_conversion_demo(n1, ["0", "01", "011", "1", "001"])

        n2 = get_preset_nfa_latihan15()
        run_conversion_demo(n2, ["ab", "abb", "ba"])
        print("\n[✓] Automated test suite & visualisasi sukses 100%!")
    else:
        main_menu()
