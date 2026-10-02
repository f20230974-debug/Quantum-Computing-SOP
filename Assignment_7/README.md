# Module 7: Error Mitigation — Lecture 0: Density Matrices, Channels & CPTP Maps

## Overview
This module introduces the mathematical framework needed to describe noise in quantum systems. Rather than working with pure state vectors, we learn to use **density matrices** — the proper formalism for describing quantum states that may be mixed (classically uncertain) or entangled with an environment we cannot access. We then derive **quantum channels** (CPTP maps) as the correct model for noisy quantum operations.

Reference Material: Prof. Indrakshi Raychowdhury's lecture notes (EM0)

---

## Key Concepts

### Density Matrices
- A density matrix $\hat{\rho}$ generalises the state vector to handle both quantum and classical uncertainty.
- Properties: Hermitian ($\hat{\rho} = \hat{\rho}^\dagger$), unit trace ($\text{Tr}\hat{\rho} = 1$), positive semidefinite ($\langle\psi|\hat{\rho}|\psi\rangle \geq 0$).
- **Purity**: $\text{Tr}(\hat{\rho}^2) = 1$ for pure states, $< 1$ for mixed states, $= 1/d$ for maximally mixed.
- **Bloch vector**: Any single-qubit state can be written as $\hat{\rho} = \frac{1}{2}(I + \vec{r} \cdot \vec{\sigma})$ where $|\vec{r}| \leq 1$.

### Partial Trace & Decoherence
- The partial trace is the quantum analogue of marginalising a joint probability distribution.
- A qubit entangled with its environment appears mixed when the environment is traced out — this is the physical origin of **decoherence**.

### Quantum Channels (CPTP Maps)
- Any physical noise process can be written in **Kraus form**: $\mathcal{E}(\hat{\rho}) = \sum_k K_k \hat{\rho} K_k^\dagger$ with $\sum_k K_k^\dagger K_k = I$.
- A map is physical if and only if it is **Completely Positive and Trace Preserving (CPTP)**.

### The Four Canonical Single-Qubit Channels
| Channel | Physics | Bloch Action |
|---|---|---|
| **Bit Flip** | X error with prob. p | Squash toward x-axis |
| **Phase Flip** | Z error with prob. p (T₂ dephasing) | Squash toward z-axis |
| **Depolarising** | Replace with I/2 with prob. p | Uniform shrinkage |
| **Amplitude Damping** | Energy loss |1⟩→|0⟩ (T₁ relaxation) | Shrink + drift to north pole |

---

## Script: `01_density_matrices_and_channels.py`

The script implements:
1. **Part 1** — Density matrices, purity, and Bloch vectors for $|0\rangle$, $|+\rangle$, and $I/2$. Partial trace of a Bell state showing that the global state is pure but the local state is maximally mixed.
2. **Part 2** — Building Kraus channels (phase flip, amplitude damping, depolarising), verifying CPTP, applying them to $|+\rangle$, and computing Pauli Transfer Matrices (PTMs).
3. **Part 3** — Solutions to all 4 exercises from the lecture notes.
4. **Part 4** — Visualization of coherence decay under the three noise channels.

## Running
```bash
python3 01_density_matrices_and_channels.py
```
