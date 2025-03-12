import os
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a 2-qubit circuit
qc = QuantumCircuit(2, 2)

# Create superposition on qubit 0
qc.h(0)

# Entangle qubit 0 and 1 (CNOT gate)
qc.cx(0, 1)

# Measure both qubits
qc.measure([0, 1], [0, 1])

# Draw the circuit
os.makedirs("images", exist_ok=True)
qc.draw('mpl')
plt.savefig("images/bell_circuit.png")
print("Circuit saved to 'images/bell_circuit.png'")

# Simulate with 500 shots
simulator = Aer.get_backend('qasm_simulator')
result = simulator.run(qc, shots=500).result()
counts = result.get_counts()

probabilities = {state: count/500 for state, count in counts.items()}

# Plot results
fig = plot_histogram(probabilities)
fig.get_axes()[0].set_ylabel("Probability")
plt.savefig("images/bell_state_results.png")
print("Results saved to 'images/bell_state_results.png'")