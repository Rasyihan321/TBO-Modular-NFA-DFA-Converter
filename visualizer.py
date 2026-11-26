"""
Modul visualizer.py
Menghasilkan visualisasi grafis (Flowchart & Diagram State Automata)
menggunakan matplotlib dan menyimpannya ke folder screenshoot/.
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Direktori penyimpanan screenshoot
BASE_DIR = Path(__file__).resolve().parent
SCREENSHOT_DIR = BASE_DIR / "laporan" / "screenshoot"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def generate_system_flowchart() -> str:
    """Menggambar Flowchart Arsitektur Sistem Modular TBO."""
    fig, ax = plt.subplots(figsize=(10, 11), dpi=200)
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 110)

    # Helper function box
    def draw_box(x, y, w, h, text, color="#e0f2fe", border="#0284c7", shape="round"):
        if shape == "round":
            box = patches.FancyBboxPatch(
                (x, y), w, h, boxstyle="round,pad=0.5,rounding_size=2",
                facecolor=color, edgecolor=border, linewidth=2
            )
        elif shape == "diamond":
            box = patches.Polygon(
                [[x + w/2, y], [x + w, y + h/2], [x + w/2, y + h], [x, y + h/2]],
                facecolor=color, edgecolor=border, linewidth=2
            )
        else:
            box = patches.Rectangle(
                (x, y), w, h,
                facecolor=color, edgecolor=border, linewidth=2
            )
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="#0f172a", wrap=True)

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(facecolor="#334155", edgecolor="#334155", width=1.5, headwidth=7, shrink=0.05)
        )
        if label:
            ax.text((x1 + x2)/2 + 2, (y1 + y2)/2, label, fontsize=8, color="#0369a1", fontweight="bold")

    # Title
    ax.text(50, 105, "FLOWCHART ARSITEKTUR SISTEM MODULAR TBO\n(NFA, DFA & SUBSET CONSTRUCTION)",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1e293b")

    # Nodes
    draw_box(37.5, 94, 25, 6, "START\n(Mulai Program)", color="#bbf7d0", border="#16a34a")
    draw_box(32.5, 82, 35, 7, "Inisialisasi Model Automata\n(DFA Engine & NFA Engine)")
    draw_arrow(50, 94, 50, 89)

    draw_box(35, 68, 30, 8, "Tampilkan Menu Utama\n1. DFA | 2. NFA\n3. Konversi | 4. Keluar")
    draw_arrow(50, 82, 50, 76)

    draw_box(32.5, 52, 35, 9, "Pilihan Menu?", shape="diamond", color="#fef08a", border="#ca8a04")
    draw_arrow(50, 68, 50, 61)

    # Cabang 1: DFA
    draw_box(5, 36, 26, 9, "MODUL DFA\nInput String -> Tracing State\nEvaluasi Final State")
    draw_arrow(32.5, 56.5, 18, 45, label="Menu 1")

    # Cabang 2: NFA
    draw_box(37, 36, 26, 9, "MODUL NFA\nInput String -> E-Closure\nTracing Subset State")
    draw_arrow(50, 52, 50, 45, label="Menu 2")

    # Cabang 3: Konversi NFA -> DFA
    draw_box(69, 36, 26, 9, "MODUL KONVERSI\nSubset Construction\nBentuk DFA Ekuivalen")
    draw_arrow(67.5, 56.5, 82, 45, label="Menu 3")

    # Titik kumpul output
    draw_box(20, 18, 60, 8, "Tampilkan Hasil: Tabel Transisi, Rute Tracing,\nStatus Penerimaan (DITERIMA / DITOLAK)")
    draw_arrow(18, 36, 35, 26)
    draw_arrow(50, 36, 50, 26)
    draw_arrow(82, 36, 65, 26)

    draw_box(37.5, 4, 25, 6, "SELESAI\n(Keluar Sistem)", color="#fecaca", border="#dc2626")
    draw_arrow(50, 18, 50, 10)

    out_path = SCREENSHOT_DIR / "flowchart_arsitektur_sistem.png"
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    return str(out_path)


def generate_subset_flowchart() -> str:
    """Menggambar Flowchart Algoritma Subset Construction."""
    fig, ax = plt.subplots(figsize=(9, 12), dpi=200)
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 120)

    def draw_box(x, y, w, h, text, color="#e0f2fe", border="#0284c7", shape="round"):
        if shape == "round":
            box = patches.FancyBboxPatch(
                (x, y), w, h, boxstyle="round,pad=0.5,rounding_size=2",
                facecolor=color, edgecolor=border, linewidth=2
            )
        elif shape == "diamond":
            box = patches.Polygon(
                [[x + w/2, y], [x + w, y + h/2], [x + w/2, y + h], [x, y + h/2]],
                facecolor=color, edgecolor=border, linewidth=2
            )
        else:
            box = patches.Rectangle(
                (x, y), w, h,
                facecolor=color, edgecolor=border, linewidth=2
            )
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="#0f172a", wrap=True)

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(facecolor="#334155", edgecolor="#334155", width=1.5, headwidth=7, shrink=0.05)
        )
        if label:
            ax.text((x1 + x2)/2 + 2, (y1 + y2)/2, label, fontsize=8, color="#0369a1", fontweight="bold")

    ax.text(50, 115, "FLOWCHART ALGORITMA SUBSET CONSTRUCTION\n(KONVERSI NFA KE DFA)",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1e293b")

    draw_box(35, 104, 30, 6, "START: NFA Input", color="#bbf7d0", border="#16a34a")
    draw_box(25, 91, 50, 8, "Hitung State Awal DFA:\nq0_DFA = E-closure({q0_NFA})\nBeri Alias Label 'A'")
    draw_arrow(50, 104, 50, 99)

    draw_box(22, 79, 56, 7, "Masukkan 'A' ke Antrean (Queue)\nInisialisasi Tabel Transisi DFA")
    draw_arrow(50, 91, 50, 86)

    draw_box(30, 64, 40, 9, "Apakah Antrean\nMasih Ada?", shape="diamond", color="#fef08a", border="#ca8a04")
    draw_arrow(50, 79, 50, 73)

    draw_box(20, 48, 60, 9, "Ambil Subset T dari Antrean\nUntuk Setiap Simbol a in Sigma:\nU = E-closure( union_{s in T} delta(s, a) )")
    draw_arrow(50, 64, 50, 57, label="Ya")

    draw_box(30, 32, 40, 9, "Apakah Subset U\nSudah Pernah Ada?", shape="diamond", color="#fed7aa", border="#ea580c")
    draw_arrow(50, 48, 50, 41)

    draw_box(5, 18, 40, 8, "Beri Label Baru pada U\n(B, C, ... atau Dead State ∅)\nMasukkan U ke Antrean")
    draw_arrow(30, 36.5, 25, 26, label="Belum")

    draw_box(55, 18, 40, 8, "Gunakan Label yang Sudah Ada\nCatat delta_DFA(T, a) = Label U")
    draw_arrow(70, 36.5, 75, 26, label="Sudah")

    draw_arrow(25, 18, 25, 12)
    draw_arrow(75, 18, 75, 12)

    # Loop back to queue check
    ax.plot([25, 25, 10, 10, 30], [12, 10, 10, 68.5, 68.5], color="#334155", linewidth=1.5)
    ax.plot([75, 75, 90, 90, 70], [12, 10, 10, 68.5, 68.5], color="#334155", linewidth=1.5)

    # Queue empty -> Finish
    draw_box(65, 50, 32, 9, "Tentukan Final State DFA:\nSemua Subset memuat F_NFA\nBentuk Objek DFA Selesai")
    draw_arrow(70, 68.5, 81, 59, label="Tidak")

    draw_box(68.5, 36, 25, 6, "SELESAI", color="#fecaca", border="#dc2626")
    draw_arrow(81, 50, 81, 42)

    out_path = SCREENSHOT_DIR / "flowchart_subset_construction.png"
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    return str(out_path)


def generate_automata_diagrams() -> dict:
    """Menggambar diagram automata representatif."""
    paths = {}

    # 1. DFA Substring 001
    fig, ax = plt.subplots(figsize=(10, 4), dpi=200)
    ax.axis("off")
    ax.set_xlim(-1, 11)
    ax.set_ylim(-2, 3)

    states = [("q0", 0, False), ("q1", 3, False), ("q2", 6, False), ("q3", 9, True)]
    for name, x, is_final in states:
        circle = patches.Circle((x, 0), 0.7, facecolor="#eff6ff", edgecolor="#2563eb", linewidth=2.5)
        ax.add_patch(circle)
        if is_final:
            inner = patches.Circle((x, 0), 0.55, facecolor="none", edgecolor="#2563eb", linewidth=1.8)
            ax.add_patch(inner)
        ax.text(x, 0, name, ha="center", va="center", fontsize=12, fontweight="bold", color="#1e3a8a")

    # Start arrow
    ax.annotate("", xy=(-0.7, 0), xytext=(-1.5, 0), arrowprops=dict(facecolor="#2563eb", width=2, headwidth=8))
    ax.text(-1.4, 0.25, "Start", fontsize=10, fontweight="bold", color="#2563eb")

    # Transitions
    ax.annotate("", xy=(2.3, 0), xytext=(0.7, 0), arrowprops=dict(facecolor="#334155", width=1.5, headwidth=6))
    ax.text(1.5, 0.2, "0", fontsize=11, fontweight="bold", color="#0f172a")

    ax.annotate("", xy=(5.3, 0), xytext=(3.7, 0), arrowprops=dict(facecolor="#334155", width=1.5, headwidth=6))
    ax.text(4.5, 0.2, "0", fontsize=11, fontweight="bold", color="#0f172a")

    ax.annotate("", xy=(8.3, 0), xytext=(6.7, 0), arrowprops=dict(facecolor="#334155", width=1.5, headwidth=6))
    ax.text(7.5, 0.2, "1", fontsize=11, fontweight="bold", color="#0f172a")

    # Loops
    ax.text(0, 1.2, "1 ↺", fontsize=11, fontweight="bold", color="#0f172a", ha="center")
    ax.text(6, 1.2, "0 ↺", fontsize=11, fontweight="bold", color="#0f172a", ha="center")
    ax.text(9, 1.2, "0, 1 ↺", fontsize=11, fontweight="bold", color="#0f172a", ha="center")

    # Back transition q1 -> q0 on 1
    ax.annotate("", xy=(0, -0.7), xytext=(3, -0.7),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.4", color="#dc2626", lw=1.8))
    ax.text(1.5, -1.5, "1", fontsize=11, fontweight="bold", color="#dc2626", ha="center")

    ax.set_title("Diagram Transisi DFA: Deteksi Substring '001'", fontsize=13, fontweight="bold", pad=15)
    p1 = SCREENSHOT_DIR / "diagram_dfa_substring_001.png"
    plt.tight_layout()
    plt.savefig(p1, bbox_inches="tight")
    plt.close()
    paths["dfa_001"] = str(p1)

    # 2. NFA Slide 7 Bab 6
    fig, ax = plt.subplots(figsize=(8, 4), dpi=200)
    ax.axis("off")
    ax.set_xlim(-1, 8)
    ax.set_ylim(-2, 3)

    nfa_states = [("q0", 0, False), ("q1", 3, False), ("q2", 6, True)]
    for name, x, is_final in nfa_states:
        circle = patches.Circle((x, 0), 0.7, facecolor="#fef3c7", edgecolor="#d97706", linewidth=2.5)
        ax.add_patch(circle)
        if is_final:
            inner = patches.Circle((x, 0), 0.55, facecolor="none", edgecolor="#d97706", linewidth=1.8)
            ax.add_patch(inner)
        ax.text(x, 0, name, ha="center", va="center", fontsize=12, fontweight="bold", color="#78350f")

    # Start arrow
    ax.annotate("", xy=(-0.7, 0), xytext=(-1.5, 0), arrowprops=dict(facecolor="#d97706", width=2, headwidth=8))
    ax.text(-1.4, 0.25, "Start", fontsize=10, fontweight="bold", color="#d97706")

    # Transitions q0 -> q1 on 0, loop on 0
    ax.annotate("", xy=(2.3, 0), xytext=(0.7, 0), arrowprops=dict(facecolor="#334155", width=1.5, headwidth=6))
    ax.text(1.5, 0.2, "0", fontsize=11, fontweight="bold", color="#0f172a")
    ax.text(0, 1.2, "0 ↺", fontsize=11, fontweight="bold", color="#0f172a", ha="center")

    # q1 -> q2 on 1, loop on 1
    ax.annotate("", xy=(5.3, 0), xytext=(3.7, 0), arrowprops=dict(facecolor="#334155", width=1.5, headwidth=6))
    ax.text(4.5, 0.2, "1", fontsize=11, fontweight="bold", color="#0f172a")
    ax.text(3, 1.2, "1 ↺", fontsize=11, fontweight="bold", color="#0f172a", ha="center")

    # q2 loop on 0,1
    ax.text(6, 1.2, "0, 1 ↺", fontsize=11, fontweight="bold", color="#0f172a", ha="center")

    ax.set_title("Diagram Transisi NFA: Contoh Utama Bab 6 Slide 7 (Σ={0,1})", fontsize=12, fontweight="bold", pad=15)
    p2 = SCREENSHOT_DIR / "diagram_nfa_contoh_utama.png"
    plt.tight_layout()
    plt.savefig(p2, bbox_inches="tight")
    plt.close()
    paths["nfa_slide7"] = str(p2)

    return paths


if __name__ == "__main__":
    p_sys = generate_system_flowchart()
    p_sub = generate_subset_flowchart()
    p_dia = generate_automata_diagrams()
    print("Flowcharts & Diagrams successfully generated!")
