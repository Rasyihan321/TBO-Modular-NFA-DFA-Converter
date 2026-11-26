"""
Modul nfa_simulator.py
Implementasi Non-deterministik Finite Automata (NFA) secara modular.
Mendukung transisi multi-state dan transisi epsilon (epsilon-move).
"""

from typing import Dict, Set, Tuple, List, Optional


class NFA:
    """
    Kelas representasi Non-deterministik Finite Automata (NFA).
    
    5-Tuple:
    - Q: Himpunan hingga state
    - sigma: Alfabet input
    - delta: Fungsi transisi Q x (Sigma U {eps}) -> P(Q)
    - q0: State awal (q0 in Q)
    - F: Himpunan state akhir (F subseteq Q)
    """

    def __init__(
        self,
        name: str,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[Tuple[str, str], Set[str]],
        start_state: str,
        final_states: Set[str],
        epsilon_symbol: str = "ε"
    ):
        self.name = name
        self.states = sorted(list(states))
        self.alphabet = sorted(list(alphabet))
        self.transitions = {k: set(v) for k, v in transitions.items()}
        self.start_state = start_state
        self.final_states = set(final_states)
        self.eps = epsilon_symbol
        self._validate()

    def _validate(self) -> None:
        """Memvalidasi integritas tuple NFA."""
        if self.start_state not in self.states:
            raise ValueError(f"State awal '{self.start_state}' tidak ada dalam himpunan Q.")
        for f in self.final_states:
            if f not in self.states:
                raise ValueError(f"State akhir '{f}' tidak ada dalam himpunan Q.")

    def get_raw_transition(self, state: str, symbol: str) -> Set[str]:
        """Mengambil himpunan state tujuan langsung dari (state, symbol)."""
        return self.transitions.get((state, symbol), set())

    def epsilon_closure(self, states: Set[str]) -> Set[str]:
        """
        Menghitung epsilon-closure dari suatu himpunan state.
        E-closure(T) = himpunan state yang dapat dicapai dari T tanpa membaca input.
        """
        closure = set(states)
        stack = list(states)

        while stack:
            st = stack.pop()
            eps_targets = self.get_raw_transition(st, self.eps)
            for target in eps_targets:
                if target not in closure:
                    closure.add(target)
                    stack.append(target)

        return closure

    def step(self, current_states: Set[str], symbol: str) -> Set[str]:
        """
        Menghitung himpunan state berikutnya setelah membaca 1 simbol dari himpunan state aktif.
        delta*(T, a) = e_closure( union_{s in T} delta(s, a) )
        """
        targets = set()
        for st in current_states:
            targets.update(self.get_raw_transition(st, symbol))
        return self.epsilon_closure(targets)

    def simulate(self, input_string: str) -> Tuple[bool, List[Dict[str, str]], Set[str]]:
        """
        Menelusuri string input pada NFA dengan melacak cabang state aktif.
        
        Returns:
            accepted (bool): True jika salah satu state aktif akhir berada di F.
            trace (list): Riwayat penelusuran subset state aktif pada setiap langkah.
            final_states (set): Himpunan state aktif saat pembacaan selesai.
        """
        curr = self.epsilon_closure({self.start_state})
        trace = []

        curr_fmt = "{" + ", ".join(sorted(curr)) + "}" if curr else "∅"

        if input_string == "" or input_string == self.eps:
            accepted = bool(curr.intersection(self.final_states))
            trace.append({
                "step": "0",
                "current": curr_fmt,
                "symbol": "ε",
                "next": curr_fmt,
                "accepted": str(accepted),
                "note": "String kosong dievaluasi dari e-closure state awal"
            })
            return accepted, trace, curr

        for i, char in enumerate(input_string, 1):
            if char not in self.alphabet:
                trace.append({
                    "step": str(i),
                    "current": curr_fmt,
                    "symbol": char,
                    "next": "∅",
                    "accepted": "False",
                    "note": f"Simbol '{char}' di luar alfabet input"
                })
                return False, trace, set()

            nxt = self.step(curr, char)
            nxt_fmt = "{" + ", ".join(sorted(nxt)) + "}" if nxt else "∅"
            has_final = bool(nxt.intersection(self.final_states))

            trace.append({
                "step": str(i),
                "current": curr_fmt,
                "symbol": char,
                "next": nxt_fmt,
                "accepted": str(has_final),
                "note": f"State aktif transisi via '{char}'"
            })
            curr = nxt
            curr_fmt = nxt_fmt

            if not curr:
                # Masuk dead state (himpunan kosong)
                break

        accepted = bool(curr.intersection(self.final_states))
        return accepted, trace, curr

    def display_table(self) -> str:
        """Menghasilkan teks tabel transisi NFA."""
        cols = list(self.alphabet)
        has_eps = any(k[1] == self.eps for k in self.transitions.keys())
        if has_eps:
            cols.append(self.eps)

        lines = []
        header = f"{'State':^14} | " + " | ".join(f"{sym:^12}" for sym in cols) + " | Status"
        sep = "-" * len(header)
        lines.append(f"\n=== Tabel Transisi NFA: {self.name} ===")
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

            for sym in cols:
                targets = self.get_raw_transition(st, sym)
                if targets:
                    cell = "{" + ",".join(sorted(targets)) + "}"
                else:
                    cell = "∅"
                row.append(f"{cell:^12}")

            status = "FINAL" if st in self.final_states else "Normal"
            row.append(f"{status:^8}")
            lines.append(" | ".join(row))

        lines.append(sep)
        return "\n".join(lines)
