from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Initialize service (assumes credentials are already saved)
service = QiskitRuntimeService()

# Create Bell state circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Draw circuit
qc.draw('mpl', filename="bell_circuit_real.png")
plt.close()
print("Circuit saved to 'bell_circuit_real.png'")

# Get available backends
backends = service.backends()
print("Available backends:", [b.name for b in backends])

# Check backend availability
if not backends:
    raise RuntimeError("No real quantum devices available. Check your IBM Quantum account")

# Select least busy backend
backend = min(backends, key=lambda x: x.status().pending_jobs)
print(f"Using backend: {backend.name}")

# Transpile circuit
transpiled_qc = transpile(qc, backend=backend)

# Submit job
with Session(backend=backend) as session:
    sampler = Sampler(mode=session)
    job = sampler.run([transpiled_qc], shots=500)
    sampler_result = job.result()

# Retrieve the measurement counts
counts = sampler_result[0].data.c.get_counts()
probabilities = {state: count/500 for state, count in counts.items()}

fig = plot_histogram(probabilities, title="Measurement Results")
fig.get_axes()[0].set_ylabel("Probability")
fig.savefig("bell_state_results_real.png", bbox_inches="tight")
print("Results saved to 'bell_state_results_real.png'")