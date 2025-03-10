from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Initialize service (credentials must be saved first)
service = QiskitRuntimeService()

def deutsch_jozsa_circuit(oracle: QuantumCircuit) -> QuantumCircuit:
    """Create a Deutsch-Jozsa circuit for a 3-input function (4 total qubits)."""
    n = 3  # Number of input qubits
    qc = QuantumCircuit(n+1, n)  # 4 qubits, 3 classical bits
    
    # Initialize ancilla qubit to |1>
    qc.x(n)
    qc.h(n)
    
    # Apply Hadamard to all input qubits
    for qubit in range(n):
        qc.h(qubit)
    
    # Append the oracle
    qc.compose(oracle, inplace=True)
    
    # Apply Hadamard to input qubits again
    for qubit in range(n):
        qc.h(qubit)
    
    # Measure input qubits
    qc.measure(range(n), range(n))
    return qc

def constant_oracle() -> QuantumCircuit:
    oracle = QuantumCircuit(4)
    oracle.x(3)
    return oracle

def balanced_oracle() -> QuantumCircuit:
    oracle = QuantumCircuit(4)
    oracle.cx(0, 3)
    oracle.cx(1, 3)
    oracle.cx(2, 3)
    return oracle

# Example usage with a constant oracle
oracle = constant_oracle()  # Change to balanced_oracle() for balanced case
dj_circuit = deutsch_jozsa_circuit(oracle)

# Draw the full circuit
dj_circuit.draw('mpl', filename="deutsch_jozsa_circuit.png")
plt.close()
print("Circuit saved to 'deutsch_jozsa_circuit.png'")

# Get backend
backends = service.backends()
print("Available backends:", [b.name for b in backends])
if not backends:
    raise RuntimeError("No real quantum devices available. Check your IBM Quantum account")
backend = min(backends, key=lambda x: x.status().pending_jobs)
print(f"Using backend: {backend.name}")

# Transpile circuit
transpiled_dj = transpile(dj_circuit, backend=backend)

# Run the algorithm
with Session(backend=backend) as session:
    sampler = Sampler(mode=session)
    job = sampler.run([transpiled_dj], shots=500)
    result = job.result()

# Analyze results
counts = result[0].data.c.get_counts()
probabilities = {k: v/500 for k, v in counts.items()}

# Determine function type
if '000' in probabilities and probabilities['000'] > 0.95:
    print("Function is CONSTANT")
else:
    print("Function is BALANCED")

# Plot results
fig = plot_histogram(probabilities, title="Deutsch-Jozsa Results")
fig.get_axes()[0].set_ylabel("Probability")
fig.savefig("deutsch_jozsa_results.png", bbox_inches="tight")
print("Results saved to 'deutsch_jozsa_results.png'")