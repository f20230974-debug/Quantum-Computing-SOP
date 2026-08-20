"""
02_half_adder.py
================
Implementation and verification of a 4-qubit Quantum Half-Adder for all 4 classical input cases.
Course: ME-QST-NISQ-era Computation (Physics SOP)
BITS Pilani, Goa Campus

Circuit Layout (Little-Endian: |q3 q2 q1 q0> = |C S B A>):
- q0: Input bit A
- q1: Input bit B
- q2: Sum bit S = A ^ B (using two CNOT gates)
- q3: Carry bit C = A & B (using one Toffoli CCX gate)
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def build_half_adder(input_a: int, input_b: int) -> QuantumCircuit:
    qc = QuantumCircuit(4, 4)

    # 1. State Preparation for Inputs A and B
    if input_a == 1:
        qc.x(0)
    if input_b == 1:
        qc.x(1)
    qc.barrier()

    # 2. Carry Bit Calculation: C = A & B (Toffoli gate)
    qc.ccx(0, 1, 3)

    # 3. Sum Bit Calculation: S = A ^ B (Two CNOT gates onto q2)
    qc.cx(0, 2)
    qc.cx(1, 2)
    qc.barrier()

    # 4. Measurement
    # Mapping: q0->c0 (A), q1->c1 (B), q2->c2 (Sum), q3->c3 (Carry)
    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])
    return qc


def run_all_cases():
    simulator = AerSimulator()
    test_cases = [(0, 0), (1, 0), (0, 1), (1, 1)]

    print("=" * 65)
    print("QUANTUM HALF-ADDER VERIFICATION ACROSS ALL CLASSICAL INPUTS")
    print("=" * 65)

    for a, b in test_cases:
        qc = build_half_adder(a, b)
        job = simulator.run(qc, shots=100)
        counts = job.result().get_counts()
        
        # Read the measured bitstring |c3 c2 c1 c0> = |C S B A>
        measured_bitstring = list(counts.keys())[0]
        c_meas = int(measured_bitstring[0])  # MSB: q3 (Carry)
        s_meas = int(measured_bitstring[1])  # q2: Sum
        b_meas = int(measured_bitstring[2])  # q1: Input B
        a_meas = int(measured_bitstring[3])  # LSB: q0 (Input A)

        expected_sum = a ^ b
        expected_carry = a & b
        is_correct = (s_meas == expected_sum) and (c_meas == expected_carry)

        print(f"Inputs: A={a}, B={b} | Measured Bitstring (|CSBA>): {measured_bitstring}")
        print(f"  -> Sum (S): {s_meas} (Expected: {expected_sum})")
        print(f"  -> Carry (C): {c_meas} (Expected: {expected_carry})")
        print(f"  -> Status: {'[PASS]' if is_correct else '[FAIL]'}\n")

    # Display sample circuit diagram for (1, 1)
    sample_qc = build_half_adder(1, 1)
    print("Circuit Diagram for Inputs A=1, B=1:")
    print(sample_qc.draw(output="text"))


if __name__ == "__main__":
    run_all_cases()
