"""
01_hardware_execution.py
========================
Week 5 Assignment: Qiskit Workflow and Reproducibility Log
Course: ME-QST-NISQ-era Computation (Physics SOP)
BITS Pilani, Goa Campus

This script creates a basic Qiskit program (Bell State), executes it 
on IBM Quantum Hardware (or a local simulator if credentials are not found), 
and automatically generates a Reproducibility Log.
"""

import sys
import datetime
import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    import qiskit_ibm_runtime
    from qiskit_ibm_runtime import QiskitRuntimeService
    from qiskit_ibm_runtime import SamplerV2 as RuntimeSampler
    RUNTIME_INSTALLED = True
except ImportError:
    RUNTIME_INSTALLED = False

def create_circuit():
    """Create a simple Bell State circuit."""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    return qc

def generate_log(circuit, isa_circuit, backend, job_id, result_counts, execution_mode):
    """Generates a detailed reproducibility log markdown file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_content = f"""# Reproducibility Log

## 1. Environment Details
* **Date & Time of Execution:** {timestamp}
* **Execution Mode:** {execution_mode}
* **Qiskit Version:** `{qiskit.__version__}`
* **Qiskit IBM Runtime Version:** `{qiskit_ibm_runtime.__version__ if RUNTIME_INSTALLED else 'N/A'}`

## 2. Hardware / Backend Specifications
* **Backend Name:** `{backend.name}`
* **Backend Provider:** `{backend.provider if hasattr(backend, 'provider') else 'Local Aer'}`

## 3. Circuit Characteristics
* **Abstract Circuit Depth:** {circuit.depth()}
* **Abstract Circuit Qubits:** {circuit.num_qubits}
* **ISA (Transpiled) Circuit Depth:** {isa_circuit.depth()}
* **ISA Circuit 2-Qubit Gate Count (Depth):** {isa_circuit.depth(lambda x: x.operation.num_qubits == 2)}

## 4. Execution Details
* **Job ID:** `{job_id}`
* **Optimization Level (Transpilation):** 3 (High optimization)
* **Shots (Measurements):** 1024

## 5. Results
* **Measurement Counts:** `{result_counts}`

### Abstract Circuit
```text
{circuit.draw(output='text')}
```
"""
    with open("reproducibility_log.md", "w") as f:
        f.write(log_content)
    print("-> Reproducibility log saved to 'reproducibility_log.md'")


def main():
    print("=" * 60)
    print("WEEK 5: HARDWARE EXECUTION & REPRODUCIBILITY")
    print("=" * 60)

    # 1. Create the circuit
    print("1. Creating Bell State circuit...")
    qc = create_circuit()

    # 2. Setup Backend
    backend = None
    execution_mode = "Simulator"
    service = None

    if RUNTIME_INSTALLED:
        try:
            # Try to load saved credentials
            service = QiskitRuntimeService()
            print("Successfully authenticated with IBM Quantum!")
            print("Searching for the least busy quantum computer...")
            # Filter for real quantum hardware that is operational
            backend = service.least_busy(operational=True, simulator=False)
            execution_mode = "Real Hardware (IBM Quantum)"
            print(f"Selected Backend: {backend.name}")
        except Exception as e:
            print("\n[WARNING] IBM Quantum credentials not found or invalid.")
            print("The assignment requested running on *actual hardware* using your free IBM access.")
            print("To do this, you need to save your API token by running:")
            print("  QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')\n")
            print("Falling back to local AerSimulator for testing...")
    
    if backend is None:
        from qiskit_aer import AerSimulator
        backend = AerSimulator()
        execution_mode = "Local Simulator (Aer)"
        print(f"Selected Backend: {backend.name} (Local)")

    # 3. Transpile Circuit (Optimize)
    print("\n2. Transpiling circuit for target backend...")
    isa_circuit = transpile(qc, backend=backend, optimization_level=3)
    
    # 4. Execute (Run)
    print("3. Executing circuit...")
    if execution_mode == "Local Simulator (Aer)":
        from qiskit.primitives import StatevectorSampler
        sampler = StatevectorSampler()
        job = sampler.run([isa_circuit], shots=1024)
        job_id = "local_sim_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        result = job.result()[0]
        # Qiskit 1.0+ local sampler format
        try:
            counts = result.data.meas.get_counts()
        except AttributeError:
            counts = result.data.c.get_counts()
            
    else:
        # Running on IBM Quantum via SamplerV2
        sampler = RuntimeSampler(mode=backend)
        job = sampler.run([isa_circuit], shots=1024)
        job_id = job.job_id()
        print(f"Job ID: {job_id}")
        print("Waiting for job to complete (this may take some time in the queue)...")
        result = job.result()[0]
        # V2 Sampler results are accessed via pub result data
        counts = result.data.meas.get_counts()

    print(f"Execution complete! Results: {counts}")

    # Plot results
    labels = list(counts.keys())
    values = list(counts.values())
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color='royalblue')
    plt.title(f'Bell State Results on {backend.name}')
    plt.xlabel('Bitstrings')
    plt.ylabel('Counts')
    plt.savefig('hardware_execution_results.png')
    print("-> Plotted results saved to 'hardware_execution_results.png'")

    # 5. Generate Reproducibility Log
    print("\n4. Generating Reproducibility Log...")
    generate_log(qc, isa_circuit, backend, job_id, counts, execution_mode)
    
    print("\nDone! Review 'reproducibility_log.md' for the required submission details.")
    print("=" * 60)

if __name__ == "__main__":
    main()
