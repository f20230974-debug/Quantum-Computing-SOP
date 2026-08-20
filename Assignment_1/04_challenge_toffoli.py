"""
04_challenge_toffoli.py
=======================
Challenge 2: Decomposition and Unitary Verification of the 3-Qubit Toffoli (CCX) Gate.
Course: ME-QST-NISQ-era Computation (Physics SOP)
BITS Pilani, Goa Campus

Decomposition:
Constructs an equivalent 3-qubit circuit using 6 CNOTs and single-qubit gates (H, T, T_dagger).
Verifies the unitary operator against the standard Qiskit CCX gate.
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, process_fidelity
import numpy as np


def build_standard_toffoli() -> QuantumCircuit:
    qc = QuantumCircuit(3)
    qc.ccx(0, 1, 2)
    return qc


def build_decomposed_toffoli() -> QuantumCircuit:
    qc = QuantumCircuit(3)
    
    # 1. Hadamard on target qubit q2
    qc.h(2)
    
    # 2. CNOT network with T and T-dagger phase rotations
    qc.cx(1, 2)
    qc.tdg(2)
    qc.cx(0, 2)
    qc.t(2)
    qc.cx(1, 2)
    qc.tdg(2)
    qc.cx(0, 2)
    
    # 3. Phase corrections and Hadamard return
    qc.t(1)
    qc.t(2)
    qc.h(2)
    
    # 4. Final CNOT and single-qubit phase adjustment on controls
    qc.cx(0, 1)
    qc.t(0)
    qc.tdg(1)
    qc.cx(0, 1)
    
    return qc


def main():
    print("=" * 70)
    print("CHALLENGE 2: TOFFOLI (CCX) DECOMPOSITION & UNITARY VERIFICATION")
    print("=" * 70)

    qc_ideal = build_standard_toffoli()
    qc_decomp = build_decomposed_toffoli()

    print("\nDecomposed Toffoli Circuit:")
    print(qc_decomp.draw(output="text"))

    # Compute unitary operators for both circuits
    op_ideal = Operator(qc_ideal)
    op_decomp = Operator(qc_decomp)

    # Check equivalence (up to global phase)
    is_equivalent = op_ideal.equiv(op_decomp)
    fidelity = process_fidelity(op_ideal, op_decomp)
    matrix_diff = np.max(np.abs(op_ideal.data - op_decomp.data))

    print("\n" + "-" * 70)
    print("VERIFICATION RESULTS:")
    print("-" * 70)
    print(f"1. Operator Equivalence (op_ideal.equiv(op_decomp)) : {is_equivalent}")
    print(f"2. Process Fidelity                                 : {fidelity:.6f}")
    print(f"3. Maximum Absolute Matrix Element Difference        : {matrix_diff:.2e}")
    print("-" * 70)

    if is_equivalent:
        print("[SUCCESS] The decomposed circuit is mathematically identical to the Toffoli gate!")
    else:
        print("[FAIL] The decomposed circuit does not match the Toffoli unitary matrix.")


if __name__ == "__main__":
    main()
