"""
Modul subset_converter.py
Implementasi algoritma Subset Construction (Powerset Construction)
untuk mengonversi Non-deterministik Finite Automata (NFA) menjadi
Deterministik Finite Automata (DFA) yang ekuivalen.
"""

from typing import Dict, Set, Tuple, List, FrozenSet
from collections import deque
from nfa_simulator import NFA
from dfa_simulator import DFA


def subset_construction(nfa: NFA) -> Tuple[DFA, List[Dict[str, str]], Dict[str, str]]:
    """
    Mengonversi NFA ke DFA menggunakan metode Subset Construction.
    
    Args:
        nfa (NFA): Objek NFA yang akan dikonversi.
        
    Returns:
        dfa (DFA): Objek DFA hasil konversi yang ekuivalen.
        conversion_steps (list): Catatan log proses pembentukan state & transisi.
        state_mapping (dict): Pemetaan alias DFA (A, B, C...) ke himpunan NFA {q0, q1...}.
    """
    initial_closure = frozenset(nfa.epsilon_closure({nfa.start_state}))

    # Pemetaan subset NFA -> Label DFA tunggal (A, B, C, ...)
    subset_to_label: Dict[FrozenSet[str], str] = {}
    label_to_subset: Dict[str, FrozenSet[str]] = {}
    
    # Label generator: A, B, C, ..., Z, S1, S2, ...
    def get_label_name(index: int) -> str:
        if index < 26:
            return chr(ord('A') + index)
        return f"S{index - 25}"

    counter = 0
    start_label = get_label_name(counter)
    counter += 1

    subset_to_label[initial_closure] = start_label
    label_to_subset[start_label] = initial_closure

    # Dead state (himpunan kosong) jika muncul
    dead_state_label: str = ""

    queue = deque([initial_closure])
    visited: Set[FrozenSet[str]] = set()

    dfa_transitions: Dict[Tuple[str, str], str] = {}
    conversion_steps: List[Dict[str, str]] = []

    while queue:
        current_subset = queue.popleft()
        if current_subset in visited:
            continue
        visited.add(current_subset)

        current_label = subset_to_label[current_subset]
        curr_desc = "{" + ", ".join(sorted(current_subset)) + "}" if current_subset else "∅"

        for symbol in nfa.alphabet:
            # Hitung gabungan transisi dari seluruh state di subset
            dest_states = set()
            for st in current_subset:
                dest_states.update(nfa.get_raw_transition(st, symbol))

            # Hitung epsilon-closure dari hasil gabungan
            next_subset = frozenset(nfa.epsilon_closure(dest_states))
            next_desc = "{" + ", ".join(sorted(next_subset)) + "}" if next_subset else "∅"

            # Daftarkan subset baru jika belum ada
            if next_subset not in subset_to_label:
                new_label = get_label_name(counter)
                counter += 1
                subset_to_label[next_subset] = new_label
                label_to_subset[new_label] = next_subset
                queue.append(next_subset)
                is_new = True
            else:
                new_label = subset_to_label[next_subset]
                is_new = False

            dfa_transitions[(current_label, symbol)] = new_label

            conversion_steps.append({
                "from_label": current_label,
                "from_subset": curr_desc,
                "symbol": symbol,
                "to_label": new_label,
                "to_subset": next_desc,
                "is_new": str(is_new),
                "calculation": f"δ({curr_desc}, {symbol}) = {next_desc} => State {new_label}"
            })

    # Tentukan state akhir DFA: setiap subset yang memuat minimal 1 state akhir NFA
    dfa_final_states = set()
    for subset, label in subset_to_label.items():
        if subset.intersection(nfa.final_states):
            dfa_final_states.add(label)

    # Susun mapping string representasi untuk laporan/tampilan
    state_mapping = {}
    for label, subset in label_to_subset.items():
        st_str = "{" + ", ".join(sorted(subset)) + "}" if subset else "∅ (Dead State)"
        state_mapping[label] = st_str

    dfa_states = set(label_to_subset.keys())
    dfa_alphabet = set(nfa.alphabet)

    dfa = DFA(
        name=f"DFA_Hasil_Konversi_{nfa.name}",
        states=dfa_states,
        alphabet=dfa_alphabet,
        transitions=dfa_transitions,
        start_state=start_label,
        final_states=dfa_final_states
    )

    return dfa, conversion_steps, state_mapping
