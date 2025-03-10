from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
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

def example_oracle() -> QuantumCircuit:
    oracle = QuantumCircuit(3, name="Oracle")
    oracle.h(2)
    oracle.ccx(0, 1, 2)
    oracle.h(2)
    return oracle

# Initialize service
service = QiskitRuntimeService()

# Parameters
num_qubits = 3
iterations = math.floor((math.pi / 4) * math.sqrt(2**num_qubits))  # 1 iteration

# Create circuit
oracle = example_oracle()
search_circuit = quantum_search(num_qubits, oracle, iterations)

# Draw circuit
search_circuit.draw('mpl', filename="search_circuit.png")
plt.close()
print("Circuit saved to 'search_circuit.png'")

# Get backend
backends = service.backends()
print("Available backends:", [b.name for b in backends])
if not backends:
    raise RuntimeError("No real quantum devices available. Check your IBM Quantum account")
backend = min(backends, key=lambda x: x.status().pending_jobs)
print(f"Using backend: {backend.name}")

transpiled_search = transpile(search_circuit, backend=backend)

with Session(backend=backend) as session:
    sampler = Sampler(mode=session)
    job = sampler.run([transpiled_search], shots=1000)
    result = job.result()

# Analyze results
counts = result[0].data.c.get_counts()
probabilities = {k: v/1000 for k, v in counts.items()}

# Plot results
fig = plot_histogram(probabilities, title="Quantum Search Results")
fig.savefig("search_results.png", bbox_inches="tight")
print("Results saved to 'search_results.png'")