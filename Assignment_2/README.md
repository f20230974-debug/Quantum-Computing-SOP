# Module 2-3: Superposition with Qiskit

## Overview
This module explores **superposition**, a core quantum mechanic principle where a quantum object can exist in a combination of states until measured. We examine the differences between classical probability (like a flipping coin) and quantum superposition (which includes phase and enables interference).

Resource: [Superposition with Qiskit (IBM Quantum Learning)](https://quantum.cloud.ibm.com/learning/en/modules/quantum-mechanics/superposition-with-qiskit)

---

## Questions & Answers

### True/False Questions

1. **A quantum superposition is basically the same as a probabilistic event in classical physics, like flipping a coin.**
   → **False.** While both involve probability upon measurement, a quantum superposition also has **phase coherence**, allowing states to interfere constructively or destructively (unlike classical coin flips).

2. **The length of the Bloch vector describing the state of a single isolated qubit is always 1.**
   → **True.** The state of a single, isolated qubit is always a pure state, which maps to a point on the surface of the Bloch sphere (radius = 1).

3. **Single-qubit quantum gates do not change the length of the Bloch vector.**
   → **True.** Single-qubit quantum gates are unitary operations, which correspond to rigid rotations of the vector on the Bloch sphere, preserving its length.

### Multiple Choice Questions

1. **Select the correct Bloch vector that represents the state $|\Psi\rangle = \sqrt{\frac{1}{3}}|0\rangle + e^{i \pi / 4} \sqrt{\frac{2}{3}}|1\rangle$**
   - **Answer:** The vector would be pointing to the northern hemisphere but angled downwards since $\cos^2(\theta/2) = 1/3 \implies \theta \approx 109.5^\circ$. It has an azimuthal angle (phase) of $\phi = \pi/4$, pointing it halfway between the positive X and Y axes on the equatorial plane.

2. **The Bloch sphere describes a qubit's: (select all that apply)**
   - **Answer:** 
     - **a.** amplitude (determined by the polar angle $\theta$)
     - **c.** phase (determined by the azimuthal angle $\phi$)
     - **e.** probability of measurement outcomes (determined by the projection along the Z-axis)

### Discussion Questions

1. **Why can the state of a qubit be visualized on the Bloch sphere, but the probability distribution of a coin flip cannot?**
   - A classical coin flip is entirely described by a single probability $P(Heads)$ (since $P(Tails) = 1 - P(Heads)$), requiring only a 1D line from 0 to 1 to represent. A qubit state, however, possesses complex amplitudes involving both relative probability and a **relative phase** ($\phi$). The normalization constraint allows us to map the probability amplitude to a polar angle ($\theta$) and the phase to an azimuthal angle ($\phi$), requiring a 3D spherical surface (a 2D manifold) to visualize.

2. **Why is a coin flipping in the air not the best analogy to a quantum superposition state? What aspect of superpositions are not captured in this analogy?**
   - A coin flipping in the air relies purely on ignorance of classical variables; its outcome is determined by its initial conditions, we just don't know them. A quantum superposition is fundamentally indeterminate until measured. Furthermore, a flipping coin cannot experience **interference**. If you apply a quantum "coin flip" (Hadamard gate) twice to a $|0\rangle$ qubit, it interferes deterministically back to $|0\rangle$. Flipping a classical coin twice just yields another random result.

---

## Challenge Problem

**Task:** Use Qiskit to create a circuit that transforms the state $|0\rangle$ to the state $\frac{\sqrt{3}}{2}|0\rangle + \frac{1}{2}e^{i \frac{5\pi}{6}}|1\rangle$.

**Implementation:**
In `01_challenge_superposition.py`, we implemented this state using Qiskit's general single-qubit unitary gate $U(\theta, \phi, \lambda)$. 
The $U$ gate applied to $|0\rangle$ yields:
$$ U(\theta, \phi, \lambda)|0\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + e^{i\phi}\sin\left(\frac{\theta}{2}\right)|1\rangle $$

By matching terms to our target state:
- $\cos(\theta/2) = \sqrt{3}/2 \implies \theta/2 = \pi/6 \implies \theta = \pi/3$
- $\phi = 5\pi/6$
- $\lambda = 0$ (arbitrary, as it only affects the relative phase of $|1\rangle$, which we are not starting in)

**Results:**
The script mathematically verifies the resulting statevector and generates a visual representation of the Bloch vector (saved as `challenge_bloch_sphere.png`).

```bash
# Run the challenge script
python3 01_challenge_superposition.py
```
