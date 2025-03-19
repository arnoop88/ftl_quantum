import os
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import math
import matplotlib.pyplot as plt

def grover_diffuser(n_qubits: int) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits, name="Diffuser")
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))
    return qc

def quantum_search(num_qubits: int, oracle: QuantumCircuit, iterations: int = 1) -> QuantumCircuit:
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    for _ in range(iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(grover_diffuser(num_qubits), inplace=True)
    qc.measure(range(num_qubits), range(num_qubits))
    return qc

def oracle() -> QuantumCircuit:
    oracle = QuantumCircuit(5, name="Oracle")
    oracle.ch(0,2)
    oracle.ccx(1, 3, 2)
    oracle.ch(0,2)
    return oracle

# Parameters
num_qubits = 5
iterations = round((math.pi / 4) * math.sqrt(2 ** num_qubits / 2))

# Create circuit
search_circuit = quantum_search(num_qubits, oracle(), iterations)

# Draw circuit
os.makedirs("images", exist_ok=True)
search_circuit.draw('mpl', filename="images/search_circuit.png")
plt.close()
print("Circuit saved to 'images/search_circuit.png'")

# Use local simulator
simulator = Aer.get_backend('qasm_simulator')
transpiled_search = transpile(search_circuit, backend=simulator)

# Run simulation
result = simulator.run(transpiled_search, shots=1000).result()
counts = result.get_counts()
probabilities = {k: v/1000 for k, v in counts.items()}

# Plot results
fig = plot_histogram(probabilities, title="Quantum Search Results")
fig.savefig("images/search_results.png", bbox_inches="tight")
print("Results saved to 'images/search_results.png'")