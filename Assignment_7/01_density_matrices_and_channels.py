"""
01_density_matrices_and_channels.py
====================================
Week 7 Assignment: Error Mitigation – Lecture 0
Density Matrices, Quantum Channels & CPTP Maps

Course: ME-QST-NISQ-era Computation (Physics SOP)
BITS Pilani, Goa Campus

This script implements the hands-on tutorial from the lecture notes
and solves the exercises at the end.
"""

import numpy as np
from qiskit.quantum_info import (
    DensityMatrix, Statevector, Pauli,
    partial_trace, Kraus, SuperOp, PTM, Operator
)
from qiskit_aer.noise import (
    depolarizing_error, phase_damping_error,
    amplitude_damping_error, pauli_error
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================
# PART 1: Density Matrices, Purity, and Bloch Vectors
# (Listing 1 from the lecture notes)
# ============================================================
def part1_density_matrices():
    print("=" * 60)
    print("PART 1: Density Matrices, Purity & Bloch Vectors")
    print("=" * 60)

    # Pure states as density matrices
    rho_0    = DensityMatrix.from_label('0')           # |0><0|
    rho_plus = DensityMatrix(Statevector.from_label('+'))  # |+><+|
    rho_mix  = DensityMatrix(np.eye(2) / 2)            # I/2

    for name, rho in [('|0>', rho_0), ('|+>', rho_plus), ('I/2', rho_mix)]:
        r = [np.real(rho.expectation_value(Pauli(p))) for p in ['X', 'Y', 'Z']]
        print(f"{name:5s} purity = {rho.purity().real:.3f}  "
              f"Bloch r = ({r[0]:+.2f}, {r[1]:+.2f}, {r[2]:+.2f})")

    # Partial trace of a Bell state
    bell = Statevector.from_label('00') + Statevector.from_label('11')
    rho_AB = DensityMatrix(bell / np.sqrt(2))
    rho_A = partial_trace(rho_AB, [1])  # trace out qubit 1 (B)
    print(f"\nBell state: global purity = {round(rho_AB.purity().real, 3)}, "
          f"reduced purity = {round(rho_A.purity().real, 3)}")
    print("Reduced density matrix of qubit A:")
    print(np.round(rho_A.data, 3))
    print()


# ============================================================
# PART 2: Building and Applying Kraus Channels
# (Listing 2 from the lecture notes)
# ============================================================
def part2_kraus_channels():
    print("=" * 60)
    print("PART 2: Kraus Channels (Bit-Flip, Phase-Flip, Depolarising, Amp. Damping)")
    print("=" * 60)

    p, gamma = 0.1, 0.2

    # Build channels from explicit Kraus operators
    K_pf = Kraus([np.sqrt(1-p)*np.eye(2),
                  np.sqrt(p)*np.array([[1,0],[0,-1]])])
    K_ad = Kraus([np.array([[1,0],[0,np.sqrt(1-gamma)]]),
                  np.array([[0,np.sqrt(gamma)],[0,0]])])
    K_dep = Kraus(depolarizing_error(p, 1))

    # Check CPTP
    for name, K in [('phase flip', K_pf), ('amp. damping', K_ad), ('depolarising', K_dep)]:
        print(f"{name:14s} is CPTP: {K.is_cptp()}")

    # Apply to |+> and watch the coherence shrink
    rho_plus = DensityMatrix(Statevector.from_label('+'))
    print("\nAction on |+>:")
    for name, K in [('phase flip', K_pf), ('amp. damping', K_ad), ('depolarising', K_dep)]:
        rho_out = rho_plus.evolve(K)
        print(f"  {name:14s} -> purity = {rho_out.purity().real:.4f}, "
              f"off-diag |rho_01| = {abs(rho_out.data[0,1]):.4f}")

    # Pauli Transfer Matrices (PTMs)
    print("\nPTM of depolarising channel:")
    print(np.round(PTM(K_dep).data.real, 3))
    print("\nPTM of amplitude damping (note the (z,0) drift entry):")
    print(np.round(PTM(K_ad).data.real, 3))

    # Compose two channels: PTMs multiply
    R1 = PTM(Kraus(depolarizing_error(0.05, 1))).data.real
    R2 = PTM(Kraus(depolarizing_error(0.05, 1))).data.real
    print(f"\nTwo 5% depolarising channels -> effective shrink factor: "
          f"{round((R2 @ R1)[1,1], 4)}  (vs 1-0.05-0.05 = 0.90)")
    print()


# ============================================================
# PART 3: Exercises from the Lecture Notes
# ============================================================
def part3_exercises():
    print("=" * 60)
    print("PART 3: Exercises")
    print("=" * 60)

    # ---- Exercise 1: Bloch Vector ----
    print("\n--- Exercise 1: Bloch Vector ---")
    print("Given: rho = (1/2) * [[1.6, 0.3], [0.3, 0.4]]")
    rho_data = 0.5 * np.array([[1.6, 0.3], [0.3, 0.4]])

    # Check validity
    eigenvalues = np.linalg.eigvalsh(rho_data)
    trace_val = np.trace(rho_data)
    is_hermitian = np.allclose(rho_data, rho_data.conj().T)
    is_pos_semidef = all(eigenvalues >= -1e-10)

    print(f"  Hermitian: {is_hermitian}")
    print(f"  Trace: {trace_val:.2f}")
    print(f"  Eigenvalues: {np.round(eigenvalues, 4)}")
    print(f"  Positive semidefinite: {is_pos_semidef}")
    print(f"  => Valid density matrix: {is_hermitian and abs(trace_val - 1) < 1e-10 and is_pos_semidef}")

    # Bloch vector: rho = (I + r.sigma) / 2
    # r_x = Tr(X rho), r_y = Tr(Y rho), r_z = Tr(Z rho)
    rho_dm = DensityMatrix(rho_data)
    rx = np.real(rho_dm.expectation_value(Pauli('X')))
    ry = np.real(rho_dm.expectation_value(Pauli('Y')))
    rz = np.real(rho_dm.expectation_value(Pauli('Z')))
    r_norm = np.sqrt(rx**2 + ry**2 + rz**2)
    print(f"  Bloch vector: r = ({rx:.2f}, {ry:.2f}, {rz:.2f})")
    print(f"  |r| = {r_norm:.4f}")
    print(f"  Pure state (|r|=1)? {np.isclose(r_norm, 1.0)}")
    print(f"  Purity = {rho_dm.purity().real:.4f}  (pure if = 1)")

    # ---- Exercise 2: Partial Trace ----
    print("\n--- Exercise 2: Partial Trace ---")

    # (a) Product state |+> ⊗ |0>
    psi_product = Statevector.from_label('+').tensor(Statevector.from_label('0'))
    rho_product = DensityMatrix(psi_product)
    rho_A_product = partial_trace(rho_product, [1])
    print("  (a) Product state |+> x |0>:")
    print(f"      rho_A = \n{np.round(rho_A_product.data, 4)}")
    print(f"      Purity of rho_A = {rho_A_product.purity().real:.4f} -> {'Pure' if np.isclose(rho_A_product.purity().real, 1.0) else 'Mixed'}")

    # (b) Singlet state |Psi-> = (|01> - |10>) / sqrt(2)
    psi_singlet = (Statevector.from_label('01') - Statevector.from_label('10')) / np.sqrt(2)
    rho_singlet = DensityMatrix(psi_singlet)
    rho_A_singlet = partial_trace(rho_singlet, [1])
    print("  (b) Singlet state |Psi-> = (|01> - |10>)/sqrt(2):")
    print(f"      rho_A = \n{np.round(rho_A_singlet.data, 4)}")
    print(f"      Purity of rho_A = {rho_A_singlet.purity().real:.4f} -> {'Pure' if np.isclose(rho_A_singlet.purity().real, 1.0) else 'Mixed'}")

    # ---- Exercise 3: Kraus Completeness ----
    print("\n--- Exercise 3: Kraus Completeness for Depolarising Channel ---")
    p_val = 0.1
    I2 = np.eye(2)
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])

    K0 = np.sqrt(1 - 3*p_val/4) * I2
    K1 = np.sqrt(p_val/4) * X
    K2 = np.sqrt(p_val/4) * Y
    K3 = np.sqrt(p_val/4) * Z

    completeness = K0.conj().T @ K0 + K1.conj().T @ K1 + K2.conj().T @ K2 + K3.conj().T @ K3
    print(f"  Sum K†_k K_k = \n{np.round(completeness.real, 6)}")
    print(f"  Equals I? {np.allclose(completeness, I2)}")

    # ---- Exercise 4: Composition of Phase-Flip Channels ----
    print("\n--- Exercise 4: Composition of Phase-Flip Channels ---")
    p1, p2 = 0.1, 0.15
    p_eff_theory = 0.5 * (1 - (1 - 2*p1) * (1 - 2*p2))
    print(f"  p1 = {p1}, p2 = {p2}")
    print(f"  Theoretical p_eff = 0.5 * (1 - (1-2p1)(1-2p2)) = {p_eff_theory:.6f}")
    print(f"  Sum p1 + p2 = {p1 + p2:.6f} (approx for small p)")

    # Verify numerically via PTM composition
    K_pf1 = Kraus([np.sqrt(1-p1)*I2, np.sqrt(p1)*Z])
    K_pf2 = Kraus([np.sqrt(1-p2)*I2, np.sqrt(p2)*Z])
    R1 = PTM(K_pf1).data.real
    R2 = PTM(K_pf2).data.real
    R_composed = R2 @ R1
    shrink_factor = R_composed[1, 1]
    p_eff_numerical = 0.5 * (1 - shrink_factor)
    print(f"  Numerical p_eff (from PTM composition) = {p_eff_numerical:.6f}")
    print(f"  Match? {np.isclose(p_eff_theory, p_eff_numerical)}")


# ============================================================
# PART 4: Visualization — Coherence Decay under Dephasing
# ============================================================
def part4_visualization():
    print("\n" + "=" * 60)
    print("PART 4: Visualization — Coherence Decay")
    print("=" * 60)

    p_values = np.linspace(0, 0.5, 50)
    purities_pf = []
    purities_dep = []
    purities_ad = []
    coherences_pf = []

    rho_plus = DensityMatrix(Statevector.from_label('+'))

    for p in p_values:
        gamma = 2 * p  # map p to gamma for amplitude damping (0 to 1)

        # Phase flip
        K_pf = Kraus([np.sqrt(1-p)*np.eye(2), np.sqrt(p)*np.array([[1,0],[0,-1]])])
        rho_pf = rho_plus.evolve(K_pf)
        purities_pf.append(rho_pf.purity().real)
        coherences_pf.append(abs(rho_pf.data[0, 1]))

        # Depolarising
        K_dep = Kraus(depolarizing_error(2*p, 1))  # scale to match
        rho_dep = rho_plus.evolve(K_dep)
        purities_dep.append(rho_dep.purity().real)

        # Amplitude damping
        K_ad = Kraus([np.array([[1,0],[0,np.sqrt(1-gamma)]]),
                      np.array([[0,np.sqrt(gamma)],[0,0]])])
        rho_ad = rho_plus.evolve(K_ad)
        purities_ad.append(rho_ad.purity().real)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(p_values, purities_pf, label='Phase Flip', color='royalblue')
    ax1.plot(p_values, purities_dep, label='Depolarising', color='crimson')
    ax1.plot(p_values, purities_ad, label='Amplitude Damping', color='forestgreen')
    ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Maximally mixed')
    ax1.set_xlabel('Error probability p')
    ax1.set_ylabel('Purity Tr(ρ²)')
    ax1.set_title('Purity Decay of |+⟩ under Noise Channels')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(p_values, coherences_pf, color='royalblue', linewidth=2)
    ax2.set_xlabel('Error probability p')
    ax2.set_ylabel('|ρ₀₁| (off-diagonal coherence)')
    ax2.set_title('Coherence Decay of |+⟩ under Phase Flip')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('noise_channels_analysis.png', dpi=150)
    print("Saved visualization to 'noise_channels_analysis.png'")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    part1_density_matrices()
    part2_kraus_channels()
    part3_exercises()
    part4_visualization()
    print("\n" + "=" * 60)
    print("ALL PARTS COMPLETE.")
    print("=" * 60)
