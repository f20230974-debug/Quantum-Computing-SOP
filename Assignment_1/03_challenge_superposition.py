"""
03_challenge_superposition.py
=============================
Challenge 1: Quantum Half-Adder with Superposition Inputs demonstrating Quantum Parallelism.
Course: ME-QST-NISQ-era Computation (Physics SOP)
BITS Pilani, Goa Campus

Inputs: A = (|0> + |1>)/sqrt(2), B = (|0> + |1>)/sqrt(2)
Input Superposition: (|00> + |01> + |10> + |11>)/2
Expected Output: Equal distribution across the 4 valid arithmetic results.
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def build_superposition_half_adder() -> QuantumCircuit:
    qc = QuantumCircuit(4, 4)

    # 1. Prepare inputs A and B in equal superposition
    qc.h(0)  # Qubit 0: Input A
    qc.h(1)  # Qubit 1: Input B
    qc.barrier()

    # 2. Compute Carry: C = A & B (Toffoli CCX onto q3)
    qc.ccx(0, 1, 3)

    # 3. Compute Sum: S = A ^ B (Two CNOTs onto q2)
    qc.cx(0, 2)
    qc.cx(1, 2)
    qc.barrier()

    # 4. Measure all qubits
    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])
    return qc


def main():
    print("=" * 70)
    print("CHALLENGE 1: QUANTUM HALF-ADDER WITH SUPERPOSITION INPUTS")
    print("=" * 70)

    qc = build_superposition_half_adder()
    print("Circuit Diagram:")
    print(qc.draw(output="text"))

    # Run on AerSimulator with 10,000 shots for clean statistics
    shots = 10000
    simulator = AerSimulator()
    job = simulator.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()

    print("\n" + "-" * 70)
    print(f"Measurement Results over {shots:,} Shots:")
    print(f"{'Bitstring (|CSBA>)':<22} | {'Count':<10} | {'Observed Prob':<15} | {'Interpretation'}")
    print("-" * 70)

    interpretations = {
        "0000": "A=0, B=0 -> Sum=0, Carry=0 (0+0=0)",
        "0101": "A=1, B=0 -> Sum=1, Carry=0 (1+0=1)",
        "0110": "A=0, B=1 -> Sum=1, Carry=0 (0+1=1)",
        "1011": "A=1, B=1 -> Sum=0, Carry=1 (1+1=2)",
    }

    # Sort bitstrings
    for bitstring in sorted(counts.keys()):
        cnt = counts[bitstring]
        prob = cnt / shots
        interp = interpretations.get(bitstring, "Unknown state")
        print(f"{bitstring:<22} | {cnt:<10} | {prob * 100:>6.2f}%         | {interp}")

    print("-" * 70)
    print("Conclusion: All 4 additions (0+0, 1+0, 0+1, 1+1) were computed concurrently")
    print("in a single execution via quantum superposition and quantum parallelism!")


if __name__ == "__main__":
    main()
