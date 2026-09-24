# Reproducibility Log

## 1. Environment Details
* **Date & Time of Execution:** 2026-09-19 19:13:40
* **Execution Mode:** Real Hardware (IBM Quantum)
* **Qiskit Version:** `2.5.2`
* **Qiskit IBM Runtime Version:** `0.49.0`

## 2. Hardware / Backend Specifications
* **Backend Name:** `ibm_fez`
* **Backend Provider:** `None`

## 3. Circuit Characteristics
* **Abstract Circuit Depth:** 3
* **Abstract Circuit Qubits:** 2
* **ISA (Transpiled) Circuit Depth:** 7
* **ISA Circuit 2-Qubit Gate Count (Depth):** 2

## 4. Execution Details
* **Job ID:** `dan92tgpqrnc7398fl80`
* **Optimization Level (Transpilation):** 3 (High optimization)
* **Shots (Measurements):** 1024

## 5. Results
* **Measurement Counts:** `{'00': 521, '11': 483, '10': 5, '01': 15}`

### Abstract Circuit
```text
        ┌───┐      ░ ┌─┐   
   q_0: ┤ H ├──■───░─┤M├───
        └───┘┌─┴─┐ ░ └╥┘┌─┐
   q_1: ─────┤ X ├─░──╫─┤M├
             └───┘ ░  ║ └╥┘
meas: 2/══════════════╩══╩═
                      0  1 
```
