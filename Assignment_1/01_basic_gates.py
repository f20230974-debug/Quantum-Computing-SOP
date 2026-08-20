"""
01_basic_gates.py
=================
Demonstration of fundamental quantum gates and state transformations using Qiskit.
Course: ME-QST-NISQ-era Computation (Physics SOP)
BITS Pilani, Goa Campus
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
import numpy as np


def explore_single_qubit_gates():
    print("=" * 60)
    print("1. SINGLE-QUBIT GATES: X, H, Z, T")
    print("=" * 60)

    # State |0>
    sv0 = Statevector.from_label("0")

    # Pauli-X (Bit Flip)
    qc_x = QuantumCircuit(1)
    qc_x.x(0)
    sv_x = sv0.evolve(qc_x)
    print(f"X|0> statevector: {sv_x.data} -> State: |1>")

    # Hadamard (Superposition)
    qc_h = QuantumCircuit(1)
    qc_h.h(0)
    sv_h = sv0.evolve(qc_h)
    print(f"H|0> statevector: {np.round(sv_h.data, 4)} -> (|0> + |1>)/sqrt(2)")

    # Pauli-Z (Phase Flip on |1>)
    qc_z = QuantumCircuit(1)
    qc_z.x(0)
    qc_z.z(0)
    sv_z = sv0.evolve(qc_z)
    print(f"Z|1> statevector: {sv_z.data} -> -|1>")

    # T Gate (pi/4 Phase Shift)
    qc_t = QuantumCircuit(1)
    qc_t.h(0)
    qc_t.t(0)
    sv_t = sv0.evolve(qc_t)
    print(f"T(|+>) statevector: {np.round(sv_t.data, 4)}")


def explore_multi_qubit_gates():
    print("\n" + "=" * 60)
    print("2. MULTI-QUBIT GATES: CNOT, SWAP, TOFFOLI (CCX)")
    print("=" * 60)

    # CNOT Gate (Bell State generation)
    qc_bell = QuantumCircuit(2)
    qc_bell.h(0)
    qc_bell.cx(0, 1)
    sv_bell = Statevector.from_label("00").evolve(qc_bell)
    print(f"Bell State (|00> + |11>)/sqrt(2):\n{np.round(sv_bell.data, 4)}")

    # SWAP Gate
    qc_swap = QuantumCircuit(2)
    qc_swap.x(0)  # Prepare |01> (q1=0, q0=1)
    qc_swap.swap(0, 1)
    sv_swap = Statevector.from_label("00").evolve(qc_swap)
    print(f"\nSWAP on |01> (little-endian q1=0, q0=1) gives:\n{sv_swap.data} -> |10>")

    # Toffoli Gate (CCX)
    qc_ccx = QuantumCircuit(3)
    qc_ccx.x(0)  # Control 1 = 1
    qc_ccx.x(1)  # Control 2 = 1
    qc_ccx.ccx(0, 1, 2)  # Target = q2
    sv_ccx = Statevector.from_label("000").evolve(qc_ccx)
    print(f"\nToffoli on |110> (controls=11, target=0) gives:\n{sv_ccx.data} -> |111>")


def run_measurement_simulation():
    print("\n" + "=" * 60)
    print("3. MEASUREMENT SIMULATION WITH AERSIMULATOR")
    print("=" * 60)

    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    backend = AerSimulator()
    job = backend.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()

    print("Circuit:")
    print(qc.draw(output="text"))
    print("\nMeasurement counts (1000 shots):", counts)


if __name__ == "__main__":
    explore_single_qubit_gates()
    explore_multi_qubit_gates()
    run_measurement_simulation()
