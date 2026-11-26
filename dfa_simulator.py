"""
Modul dfa_simulator.py
Implementasi Deterministik Finite Automata (DFA) secara modular.
Didesain sesuai kaidah formal 5-tuple M = (Q, Sigma, delta, q0, F).
"""

from typing import Dict, Set, Tuple, List, Optional


class DFA:
    """
    Kelas representasi Deterministik Finite Automata (DFA).
    
    5-Tuple:
    - Q: Himpunan hingga state
    - sigma: Alfabet input
    - delta: Fungsi transisi Q x Sigma -> Q
    - q0: State awal (q0 in Q)
    - F: Himpunan state akhir (F subseteq Q)
    """

    def __init__(
        self,
        name: str,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[Tuple[str, str], str],
        start_state: str,
        final_states: Set[str]
    ):
        self.name = name
        self.states = sorted(list(states))
        self.alphabet = sorted(list(alphabet))
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = set(final_states)
        self._validate()

    def _validate(self) -> None:
        """Memvalidasi integritas 5-tuple DFA."""
        if self.start_state not in self.states:
            raise ValueError(f"State awal '{self.start_state}' tidak ada dalam himpunan Q.")
        for f in self.final_states:
            if f not in self.states:
                raise ValueError(f"State akhir '{f}' tidak ada dalam himpunan Q.")

    def get_transition(self, state: str, symbol: str) -> Optional[str]:
        """Mengambil state tujuan dari (state, symbol)."""
        return self.transitions.get((state, symbol), None)

    def simulate(self, input_string: str) -> Tuple[bool, List[Dict[str, str]], str]:
        """
        Menelusuri string input simbol demi simbol pada DFA.
        
        Returns:
            accepted (bool): True jika string diterima, False jika ditolak.
            trace (list): Riwayat langkah demi langkah transisi.
            final_state (str): State akhir tempat mesin berhenti.
        """
        curr = self.start_state
        trace = []

        if input_string == "" or input_string == "ε":
            # String kosong (epsilon)
            accepted = curr in self.final_states
            return accepted, [{"step": "0", "current": curr, "symbol": "ε", "next": curr, "note": "String kosong"}], curr

        for i, char in enumerate(input_string, 1):
            if char not in self.alphabet:
                nxt = "TRAP_REJECT"
                trace.append({
                    "step": str(i),
                    "current": curr,
                    "symbol": char,
                    "next": nxt,
                    "note": f"Simbol '{char}' di luar alfabet input"
                })
                return False, trace, nxt

            nxt = self.get_transition(curr, char)
            if nxt is None:
                trace.append({
                    "step": str(i),
                    "current": curr,
                    "symbol": char,
                    "next": "DEAD_STATE",
                    "note": "Tidak ada transisi terdefinisi"
                })
                return False, trace, "DEAD_STATE"

            trace.append({
                "step": str(i),
                "current": curr,
                "symbol": char,
                "next": nxt,
                "note": f"δ({curr}, {char}) = {nxt}"
            })
            curr = nxt

        accepted = curr in self.final_states
        return accepted, trace, curr

    def display_table(self) -> str:
        """Menghasilkan teks tabel transisi DFA."""
        lines = []
        header = f"{'State':^14} | " + " | ".join(f"{sym:^8}" for sym in self.alphabet) + " | Status"
        sep = "-" * len(header)
        lines.append(f"\n=== Tabel Transisi DFA: {self.name} ===")
        lines.append(sep)
        lines.append(header)
        lines.append(sep)

        for st in self.states:
            prefix = ""
            if st == self.start_state and st in self.final_states:
                prefix = "-> *"
            elif st == self.start_state:
                prefix = "->  "
            elif st in self.final_states:
                prefix = " *  "
            else:
                prefix = "    "

            st_label = f"{prefix}{st}"
            row = [f"{st_label:<14}"]
            for sym in self.alphabet:
                nxt = self.get_transition(st, sym) or "∅"
                row.append(f"{nxt:^8}")

            status = "FINAL" if st in self.final_states else "Normal"
            row.append(f"{status:^8}")
            lines.append(" | ".join(row))

        lines.append(sep)
        return "\n".join(lines)
