# Module 4-6: Quantum Computing Workflow / Intro to Patterns

## Overview
This module transitions from basic quantum circuits to utility-scale application structures. It introduces the **Qiskit Pattern**, a standard 4-step development workflow that breaks down domain-specific problems into manageable stages. This structure ensures quantum tasks can be optimized and executed efficiently across heterogeneous (CPU/GPU/QPU) computing infrastructure.

Resource: [Intro to Patterns (IBM Quantum Documentation)](https://quantum.cloud.ibm.com/docs/en/guides/intro-to-patterns)

---

## The 4 Steps of a Qiskit Pattern

1. **Map Problem to Quantum Circuits and Operators**
   - **What it is:** Translating a classical problem (like chemistry simulation, optimization, etc.) into a quantum format.
   - **Output:** Abstract quantum circuits and observable operators (e.g., Hamiltonians). 
   - **Consideration:** Deciding whether the output requires probability distributions (using `Sampler`) or expectation values (using `Estimator`).

2. **Optimize for Target Hardware**
   - **What it is:** Transpiling the abstract circuits into an Instruction Set Architecture (ISA) circuit. 
   - **Process:** This involves routing the circuit to match the physical qubit layout (coupling map), converting logic into the hardware's native basis gates, and minimizing the number of operations to reduce noise. 
   - **Output:** An ISA circuit that the target QPU can actually execute.

3. **Execute on Target Hardware**
   - **What it is:** Running the optimized ISA circuits on hardware using Qiskit Primitives.
   - **Primitives:** 
     - `Sampler`: Returns bitstrings/probability distributions.
     - `Estimator`: Returns expectation values of observables.
   - **Execution Modes:** `Batch` for parallel processing or `Session` for iterative/variational algorithms without queuing delays.

4. **Post-Process Results**
   - **What it is:** Using classical computing to interpret the quantum output.
   - **Process:** This can include readout error mitigation, visualizing results, computing cost functions, or extracting chemical/physical properties from the raw data.

---

## Demonstration Script

We have implemented a script `01_workflow_demonstration.py` that practically walks through all 4 steps of this pattern using a basic Bell State circuit:

- **Step 1 (Map):** Creates the abstract 2-qubit entanglement circuit.
- **Step 2 (Optimize):** Transpiles the circuit against a simulator backend.
- **Step 3 (Execute):** Uses the `StatevectorSampler` primitive to run the job.
- **Step 4 (Post-Process):** Extracts the bitstring counts, calculates classical probabilities, and generates a visual histogram.

**To run the demonstration:**
```bash
python3 01_workflow_demonstration.py
```
*(The output histogram is saved as `workflow_results.png`)*
