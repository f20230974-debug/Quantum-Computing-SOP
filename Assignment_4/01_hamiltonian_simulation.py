"""
01_hamiltonian_simulation.py
============================
Demonstration of the Hamiltonian Simulation Workflow.
Course: ME-QST-NISQ-era Computation (Physics SOP)
BITS Pilani, Goa Campus

This script follows the Qiskit Pattern to simulate the time evolution 
of a spin Hamiltonian (e.g., an Ising model) and measure an observable.

Workflow Steps:
1. MAP: Define the Hamiltonian, observable, and time evolution circuit using Trotterization.
2. OPTIMIZE: Transpile the circuit for the target backend (AerSimulator).
3. EXECUTE: Run the ISA circuit using EstimatorV2 to compute expectation values.
4. POST-PROCESS: Extract and visualize the expectation value over time.
"""

import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import StatevectorEstimator
from qiskit_aer import AerSimulator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    print("=" * 60)
    print("HAMILTONIAN SIMULATION WORKFLOW DEMONSTRATION")
    print("=" * 60)

    # ---------------------------------------------------------
    # STEP 1: MAP
    # ---------------------------------------------------------
    print("\n[Step 1: MAP]")
    
    # 1. Define the Hamiltonian (e.g., 2-qubit Transverse-field Ising Model)
    # H = J * (Z0 Z1) + h * (X0 + X1)
    # Let J = -1.0, h = -0.5
    hamiltonian = SparsePauliOp.from_list([
        ("ZZ", -1.0),
        ("XI", -0.5),
        ("IX", -0.5)
    ])
    print(f"Hamiltonian to simulate:\n{hamiltonian}")

    # 2. Define the Observable we want to measure (e.g., total magnetization in Z)
    observable = SparsePauliOp.from_list([("ZI", 1.0), ("IZ", 1.0)])
    print(f"\nObservable to measure:\n{observable}")

    # We will simulate the evolution over several time steps to plot dynamics
    time_steps = np.linspace(0, 3, 10) # t from 0 to 3
    num_trotter_steps = 3

    print(f"\nConstructing abstract time evolution circuits for {len(time_steps)} time steps...")
    abstract_circuits = []
    
    for t in time_steps:
        # Create the evolution operator for time t
        evo_gate = PauliEvolutionGate(hamiltonian, time=t, synthesis=SuzukiTrotter(reps=num_trotter_steps))
        
        # Initial state |00>
        qc = QuantumCircuit(2)
        qc.append(evo_gate, [0, 1])
        abstract_circuits.append(qc)

    print(f"Example abstract circuit (t={time_steps[-1]:.2f}):")
    print(abstract_circuits[-1].draw(output="text"))

    # ---------------------------------------------------------
    # STEP 2: OPTIMIZE
    # ---------------------------------------------------------
    print("\n[Step 2: OPTIMIZE]")
    backend = AerSimulator()
    print("Transpiling circuits to ISA format for AerSimulator...")
    isa_circuits = transpile(abstract_circuits, backend)
    
    # In Qiskit >= 1.0, observables must be laid out to match the ISA circuit layout
    isa_observable = observable.apply_layout(isa_circuits[0].layout)
    
    print(f"Example ISA circuit depth: {isa_circuits[-1].depth()}")

    # ---------------------------------------------------------
    # STEP 3: EXECUTE
    # ---------------------------------------------------------
    print("\n[Step 3: EXECUTE]")
    print("Executing ISA circuits using EstimatorV2...")
    estimator = StatevectorEstimator()
    
    # Format for EstimatorV2: list of (circuit, observables) PUBs
    pubs = [(circ, isa_observable) for circ in isa_circuits]
    job = estimator.run(pubs)
    
    print(f"Job submitted. Waiting for results...")
    result = job.result()

    # ---------------------------------------------------------
    # STEP 4: POST-PROCESS
    # ---------------------------------------------------------
    print("\n[Step 4: POST-PROCESS]")
    print("Extracting expectation values...")
    
    # Extract expectation values from the pub results
    expectation_values = [pub_result.data.evs for pub_result in result]
    
    print("Expectation values over time:")
    for t, ev in zip(time_steps, expectation_values):
        print(f"t = {t:.2f} | <O> = {ev:.4f}")

    # Plot the results
    plt.figure(figsize=(8, 5))
    plt.plot(time_steps, expectation_values, marker='o', linestyle='-', color='teal')
    plt.xlabel("Time (t)")
    plt.ylabel("Expectation Value $\\langle Z_0 + Z_1 \\rangle$")
    plt.title("Hamiltonian Simulation: Transverse-field Ising Model")
    plt.grid(True, alpha=0.3)
    plt.savefig('hamiltonian_simulation_plot.png')
    
    print("\nSaved plot to 'hamiltonian_simulation_plot.png'.")
    print("=" * 60)

if __name__ == "__main__":
    main()
