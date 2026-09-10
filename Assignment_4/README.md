# Module 7-9: Hamiltonian Simulation Workflow

## Overview
This module demonstrates how to apply the Qiskit Patterns workflow to a practical physics problem: simulating the time evolution of a quantum system governed by a specific Hamiltonian. This is one of the most natural applications of quantum computers (quantum simulation).

Resource: [Function Template: Hamiltonian Simulation (IBM Quantum Documentation)](https://quantum.cloud.ibm.com/docs/en/guides/function-template-hamiltonian-simulation)

---

## The Workflow Implementation

In `01_hamiltonian_simulation.py`, we implemented a localized version of the Hamiltonian Simulation workflow using the Qiskit Pattern structure.

### 1. Map
- **Hamiltonian:** We define a 2-qubit Transverse-Field Ising Model using `SparsePauliOp`. The Hamiltonian is $H = -J(Z_0 Z_1) - h(X_0 + X_1)$, representing interacting spins in an external magnetic field.
- **Observable:** We define an observable to measure the total magnetization in the Z-direction: $\mathcal{O} = Z_0 + Z_1$.
- **Circuit Generation:** We use `PauliEvolutionGate` along with the `SuzukiTrotter` synthesis algorithm to approximate the time-evolution operator $e^{-iHt}$ into a sequence of abstract logic gates for various time steps ($t=0$ to $t=3$).

### 2. Optimize
- The abstract Trotterized circuits are transpiled using standard Qiskit transpilation against our local simulator (`AerSimulator`). 
- This reduces the circuit to an Instruction Set Architecture (ISA) containing only basis gates supported by the simulator and ensures the observable is properly mapped to the transpiled layout. 
- *Note:* In utility-scale workflows, advanced add-ons like `AQC-Tensor` are used in this step to compress the initial layers of Trotter steps using Matrix Product States (MPS) to reduce overall circuit depth.

### 3. Execute
- We use the `StatevectorEstimator` primitive (part of the Qiskit V2 Primitives) to run the ISA circuits.
- The Estimator takes a list of PUBs (Primitive Unified Blocs), where each PUB consists of a circuit and our target observable. It calculates the expectation value $\langle \psi(t) | \mathcal{O} | \psi(t) \rangle$.

### 4. Post-Process
- We iterate through the job results, extracting the computed expectation values.
- We classically plot the time evolution of the magnetization $\langle Z_0 + Z_1 \rangle$, visualizing the oscillating quantum dynamics of the spin system.

---

## Running the Simulation

```bash
# Run the local Hamiltonian simulation script
python3 01_hamiltonian_simulation.py
```
*(The output plot will be saved as `hamiltonian_simulation_plot.png`)*
