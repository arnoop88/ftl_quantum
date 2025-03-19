# Quantum Computing Algorithms with Qiskit

A collection of quantum algorithms implemented using Qiskit and IBM Quantum Runtime, as part of the FTL_quantum project. This repository includes solutions to exercises on superposition, entanglement, noise, and advanced algorithms like Shor's factorization.

---

## 📋 Table of Contents

- [Implemented Scripts](#-implemented-scripts)
- [Bonus Algorithms](#-bonus-algorithms)
- [Setup](#%EF%B8%8F-setup)
- [Usage](#-usage)
- [Results Interpretation](#-results-interpretation)

---

## 📜 Implemented Scripts

0. **Token**
   - Save your IBM quantum API token to your computer (`save_token.py`).
1. **List**
   - List all local simulators and available quantum simulators (`list.py`).
2. **Superposition**
   - Create a single-qubit superposition state (`superposition.py`).
3. **Entanglement**
   - Bell state circuit with visualization (`entanglement.py`).
4. **Quantum Noise**
   - Compare simulator vs. real quantum hardware results (`quantum_noise.py`).
5. **Deutsch-Jozsa**
   - Determine if a function is constant/balanced (`deutsch-jozsa.py`).
6. **Search Algorithm**
   - Grover's algorithm for unstructured search (`search_algorithm.py`).

## 🏆 Bonus Algorithms

1. **Bernstein-Vazirani**
   - Find a hidden bitstring (`bernstein_vazirani.py`).
2. **Simon's Algorithm**
   - Identify a periodic hidden string (`simon.py`).
3. **Shor's Algorithm**
   - Simplified factorization of `N = 15` (`shor.py`).
4. **Quantum Phase Estimation (QPE)**
   - Estimate the eigenphase of a unitary operator (`qpe.py`).
5. **Variational Quantum Eigensolver (VQE)**
   - Find the ground state energy of a Hamiltonian (`vqe.py`).

---

## ⚙️ Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **IBM Quantum API Token**
   - Replace `YOUR_API_TOKEN` by your actual API token in `save_token.py`.
   - Run the script (`save_token.py`).

## 🚀 Usage

- Run any script
- Outputs:
  - Circuit diagrams (e.g., `images/shor_circuit.png`).
  - Measurement histograms (e.g., `images/shor_results.png`).

## 📊 Results Interpretation

- **Simulator vs. Hardware**

  - Results from simulators will show near-ideal probabilities, while real quantum devices will include noise-induced errors (e.g., extra states like `01` in Bell state results).

- **Key Outputs**
  - **Simon's Algorithm**:
    - Measurements (e.g., `001`, `110`) will satisfy `y·s = 0 mod 2`
    - Use Gaussian elimination on valid measurements to solve for the hidden string `s`
  - **Shor's Algorithm**:
    - Look for dominant measurements like `0100` (binary for 4), which represent the period `r`
    - Compute factors using `gcd(a^(r/2) ± 1, N)`
  - **VQE**:
    - Optimal parameters represent angles in the ansatz circuit
    - Energy close to `-1.0` indicates successful ground state preparation

---

**Note**:

- IBM Quantum access requires a [free account](https://quantum-computing.ibm.com/).
- Real hardware results may vary significantly due to quantum noise and limited qubit coherence times.
