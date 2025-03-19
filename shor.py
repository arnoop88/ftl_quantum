import numpy as np
import os
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT, UnitaryGate
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def mod_mult_unitary(a: int, N: int, n: int) -> np.ndarray:
    dim = 2 ** n
    U = np.zeros((dim, dim), dtype=complex)
    for y in range(dim):
        if y < N:
            result = (a * y) % N
        else:
            result = y
        U[result, y] = 1
    return U

def shor_circuit_custom(N: int, a: int, t: int = 4, n: int = 4) -> QuantumCircuit:
    qc = QuantumCircuit(t + n, t)
    qc.h(range(t))
    qc.x(t + n - 1)

    for j in range(t):
        factor = pow(a, 2 ** j, N)
        U = mod_mult_unitary(factor, N, n)
        mult_gate = UnitaryGate(U, label=f"Mult_{factor}")
        c_mult_gate = mult_gate.control(1)
        qc.append(c_mult_gate, [j] + list(range(t, t + n)))
    
    qc.append(QFT(t, inverse=True, do_swaps=True), range(t))
    qc.measure(range(t), range(t))
    
    return qc

N = 15
a = 7
t = 4
n = 4

shor_qc = shor_circuit_custom(N, a, t, n)

# Save circuit diagram
os.makedirs("images", exist_ok=True)
shor_qc.draw('mpl', filename="images/shor_circuit.png")
plt.close()
print("Circuit saved to 'images/shor_circuit.png'")

# Use local simulator
simulator = Aer.get_backend('qasm_simulator')
transpiled_shor = transpile(shor_qc, backend=simulator)

# Run simulation
result = simulator.run(transpiled_shor, shots=1000).result()
counts = result.get_counts()
probabilities = {k: v / 1000 for k, v in counts.items()}

# Plot results
fig = plot_histogram(probabilities, title="Shor's Algorithm Results")
fig.savefig("images/shor_results.png", bbox_inches="tight")
print("Results saved to 'images/shor_results.png'")
