"""
01_workflow_demonstration.py
============================
Demonstration of the 4 steps of a Qiskit Pattern (Quantum Computing Workflow).
Course: ME-QST-NISQ-era Computation (Physics SOP)
BITS Pilani, Goa Campus

The 4 steps:
1. Map: Define the problem as quantum circuits and operators.
2. Optimize: Transpile the circuit for target hardware (ISA circuit).
3. Execute: Run on target hardware using Primitives (Sampler/Estimator).
4. Post-process: Analyze and visualize the results.
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.primitives import StatevectorSampler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    print("=" * 60)
    print("QISKIT PATTERNS WORKFLOW DEMONSTRATION")
    print("=" * 60)

    # ---------------------------------------------------------
    # STEP 1: MAP
    # ---------------------------------------------------------
    print("\n[Step 1: MAP]")
    print("Creating a Bell state circuit to represent our problem.")
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    print("Abstract Circuit:")
    print(qc.draw(output="text"))

    # ---------------------------------------------------------
    # STEP 2: OPTIMIZE
    # ---------------------------------------------------------
    print("\n[Step 2: OPTIMIZE]")
    print("Transpiling the circuit to an Instruction Set Architecture (ISA).")
    # For demonstration, we'll use the local AerSimulator as our "target hardware"
    simulator = AerSimulator()
    isa_circuit = transpile(qc, simulator)
    print("Optimized ISA Circuit:")
    print(isa_circuit.draw(output="text"))

    # ---------------------------------------------------------
    # STEP 3: EXECUTE
    # ---------------------------------------------------------
    print("\n[Step 3: EXECUTE]")
    print("Executing the ISA circuit using the Sampler primitive.")
    # In Qiskit 1.0+, we use Primitives (Sampler V2) for execution
    sampler = StatevectorSampler()
    # Run the circuit and get the job
    job = sampler.run([isa_circuit], shots=1024)
    # Get the result for the first (and only) pub
    result = job.result()[0]
    
    # ---------------------------------------------------------
    # STEP 4: POST-PROCESS
    # ---------------------------------------------------------
    print("\n[Step 4: POST-PROCESS]")
    print("Analyzing the measurement results.")
    # Extract bitstring counts from the measurement output
    # Depending on Qiskit version, Sampler V2 returns data in a BitArray
    try:
        counts = result.data.meas.get_counts()
    except AttributeError:
        # Fallback if different format
        counts = result.data.c.get_counts()

    print("Measurement Counts:", counts)
    
    # Simple classical post-processing: calculate probabilities
    total_shots = sum(counts.values())
    for bitstring, count in counts.items():
        prob = count / total_shots
        print(f"State |{bitstring}> : Probability {prob:.2%}")

    # Visualize
    labels = list(counts.keys())
    values = list(counts.values())
    plt.bar(labels, values, color='cornflowerblue')
    plt.xlabel('Bitstrings')
    plt.ylabel('Counts')
    plt.title('Bell State Measurement Results')
    plt.savefig('workflow_results.png')
    print("\nSaved histogram to 'workflow_results.png'.")
    print("=" * 60)

if __name__ == "__main__":
    main()
