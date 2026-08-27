"""
01_challenge_superposition.py
=============================
Challenge Problem: Transform the |0> state to (sqrt(3)/2)|0> + (1/2)exp(i 5pi/6)|1>
Course: ME-QST-NISQ-era Computation (Physics SOP)
BITS Pilani, Goa Campus

We use the general U-gate: U(theta, phi, lambda).
Applied to |0>, the state becomes: cos(theta/2)|0> + exp(i phi) * sin(theta/2)|1>
Therefore:
cos(theta/2) = sqrt(3)/2  => theta/2 = pi/6 => theta = pi/3
phi = 5pi/6
lambda = 0 (irrelevant when applied to |0>)
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def build_challenge_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(1)
    
    # Calculate angles
    theta = np.pi / 3
    phi = 5 * np.pi / 6
    lam = 0
    
    # Apply U gate
    qc.u(theta, phi, lam, 0)
    return qc

def main():
    print("=" * 60)
    print("CHALLENGE: CREATING A SPECIFIC SUPERPOSITION STATE")
    print("=" * 60)
    
    qc = build_challenge_circuit()
    print("Circuit Diagram:")
    print(qc.draw(output="text"))
    
    state = Statevector.from_instruction(qc)
    print("\nResulting Statevector:")
    print(np.round(state.data, 4))
    
    # Verify mathematically
    expected_0 = np.sqrt(3)/2
    expected_1 = 0.5 * np.exp(1j * 5 * np.pi / 6)
    expected_state = np.array([expected_0, expected_1])
    
    print("\nExpected Statevector:")
    print(np.round(expected_state, 4))
    
    if np.allclose(state.data, expected_state):
        print("\n[SUCCESS] The generated state matches the expected state!")
    else:
        print("\n[FAIL] The states do not match.")

    # Save bloch sphere visualization
    fig = plot_bloch_multivector(state)
    fig.savefig('challenge_bloch_sphere.png')
    print("\nSaved Bloch sphere visualization to 'challenge_bloch_sphere.png'.")

if __name__ == "__main__":
    main()
