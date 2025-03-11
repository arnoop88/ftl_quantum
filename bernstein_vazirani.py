from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def bv_oracle(secret_string: str) -> QuantumCircuit:
    n = len(secret_string)
    oracle = QuantumCircuit(n + 1)
    for qubit, bit in enumerate(reversed(secret_string)):
        if bit:
            oracle.cx(qubit, n)
    return oracle

def bernstein_vazirani(secret_string: str) -> QuantumCircuit:
    n = len(secret_string)
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(n)
    qc.h(range(n))
    oracle = bv_oracle(secret_string)
    qc.compose(oracle, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

service = QiskitRuntimeService()

secret = "101"  # Secret string to find
bv_circuit = bernstein_vazirani(secret)

bv_circuit.draw('mpl', filename="bv_circuit.png")
plt.close()
print("Circuit saved to 'bv_circuit.png'")

backends = service.backends(simulator=False, operational=True)
if not backends:
    raise RuntimeError("No real quantum devices available. Check your IBM Quantum account")
backend = min(backends, key=lambda x: x.status().pending_jobs)
print(f"Using backend: {backend.name}")

transpiled_bv = transpile(bv_circuit, backend=backend)

with Session(backend=backend) as session:
    sampler = Sampler(mode=session)
    job = sampler.run([transpiled_bv], shots=1000)
    result = job.result()

counts = result[0].data.c.get_counts()
probabilities = {k: v/1000 for k, v in counts.items()}

fig = plot_histogram(probabilities, title="Bernstein-Vazirani Results")
fig.savefig("bv_results.png", bbox_inches="tight")
print("Results saved to 'bv_results.png'")

# Print most probable result
most_probable = max(probabilities, key=probabilities.get)
print(f"Secret string found: {most_probable}")