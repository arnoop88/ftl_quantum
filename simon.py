import os
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def bdotz(b, z):
    accum = 0
    for i in range(len(b)):
        accum += int(b[i]) * int(z[i])
    return (accum % 2)

def simon_oracle(secret_string: str) -> QuantumCircuit:
    n = len(secret_string)
    qc = QuantumCircuit(2*n)
    for i in range(n):
        qc.cx(i, i+n)
    for i, bit in enumerate(secret_string):
        if bit == '1':
            qc.cx(0, i+n)
    return qc

def simon_algorithm(secret_string: str) -> QuantumCircuit:
    n = len(secret_string)
    qc = QuantumCircuit(2*n, n)
    qc.h(range(n))
    oracle = simon_oracle(secret_string)
    qc.compose(oracle, inplace=True)
    qc.barrier
    qc.h(range(n))
    qc.measure(range(n), list(reversed(range(n))))
    return qc

service = QiskitRuntimeService()

secret = "101"  
simon_circ = simon_algorithm(secret)

os.makedirs("images", exist_ok=True)
simon_circ.draw('mpl', filename="images/simon_circuit.png")
plt.close()
print("Circuit saved to 'images/simon_circuit.png'")

backends = service.backends(simulator=False, operational=True)
if not backends:
    raise RuntimeError("No real quantum devices available. Check your IBM Quantum account")
backend = min(backends, key=lambda x: x.status().pending_jobs)
print(f"Using backend: {backend.name}")

transpiled_simon = transpile(simon_circ, backend=backend)

with Session(backend=backend) as session:
    sampler = Sampler(mode=session)
    job = sampler.run([transpiled_simon], shots=1000)
    result = job.result()

counts = result[0].data.c.get_counts()
probabilities = {k: v/1000 for k, v in counts.items()}

fig = plot_histogram(probabilities, title="Simon's Algorithm Results")
fig.savefig("images/simon_results.png", bbox_inches="tight")
print("Results saved to 'images/simon_results.png'")

for z in counts:
    print('{} ⋅ {} = {} (mod 2)'.format(secret, z, bdotz(secret, z)))
