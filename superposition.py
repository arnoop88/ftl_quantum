from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create quantum circuit
qc = QuantumCircuit(1, 1)

# Add H gate
qc.h(0)
qc.measure(0, 0)

# Draw and save circuit
qc.draw('mpl')
plt.savefig("circuit_visualization.png")
print("Circuit diagram saved to 'circuit_visualization.png'")

# Simulate with 500 shots
simulator = Aer.get_backend('qasm_simulator')
result = simulator.run(qc, shots=500).result()
counts = result.get_counts()

# Convert counts to probabilities
probabilities = {state: count/500 for state, count in counts.items()}

# Plot probability distribution
fig = plot_histogram(probabilities)
fig.get_axes()[0].set_ylabel("Probability")
plt.savefig("probability_distribution.png")
print("Measurement probabilities saved to 'probability_distribution.png'")