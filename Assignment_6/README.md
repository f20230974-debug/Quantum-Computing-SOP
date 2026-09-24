# Module 6: Hardware Execution & Reproducibility Logs

## Overview
This module transitions from local simulation to actual hardware execution. As per Prof. Indrakshi's instructions, the core task is to understand the complete workflow of a quantum computing task on real hardware and learn how to maintain a strict reproducibility log.

Resource: [Quantum Computing in Practice](https://quantum.cloud.ibm.com/learning/en/courses/quantum-computing-in-practice)

---

## Assignment Implementation

In `01_hardware_execution.py`, we implemented a robust pipeline that prepares a Qiskit program, attempts to authenticate with IBM Quantum, executes the job, and automatically generates the required documentation.

### The Qiskit Program
We chose a foundational quantum circuit for this tutorial: generating a **Bell State** (a maximally entangled 2-qubit state).
- The circuit utilizes a Hadamard ($H$) gate on Qubit 0, followed by a Controlled-NOT ($CX$) gate between Qubit 0 and 1.
- This creates the state $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$.

### Workflow Features
1. **Hardware Authentication:** The script securely leverages the `QiskitRuntimeService` to connect to IBM's quantum fleet. 
2. **Dynamic Backend Selection:** If authenticated, the script queries IBM's API to find the *least busy operational quantum computer* to minimize queue times. (If credentials are not found, it gracefully falls back to a local `AerSimulator` for testing).
3. **Execution with Primitives:** Transpiles the circuit and executes it using the advanced `SamplerV2` primitive.
4. **Automated Documentation:** After execution, the script dynamically writes `reproducibility_log.md` detailing the exact environment, hardware state, and job parameters used.

## Instructions for Real Hardware Execution

If the script runs on the local simulator but you want to run it on actual hardware for the final submission, you must save your IBM Quantum API key locally first:

1. Copy your API token from your [IBM Quantum Dashboard](https://quantum.cloud.ibm.com/).
2. Open a python terminal and run:
   ```python
   from qiskit_ibm_runtime import QiskitRuntimeService
   QiskitRuntimeService.save_account(channel="ibm_quantum", token="<YOUR_TOKEN>")
   ```
3. Run the script again:
   ```bash
   python3 01_hardware_execution.py
   ```
The script will detect the saved account, route the job to a real QPU, and wait for it in the queue before updating the log.
