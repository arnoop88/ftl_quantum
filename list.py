from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer import Aer

# Initialize the runtime service (automatically loads saved account)
service = QiskitRuntimeService()

# List local quantum simulators
print("Local Quantum Simulators:")
for simulator in Aer.backends():
    print(f"	{simulator}")

# List available quantum computers
print("\nAvailable Quantum Computers:")
for backend in service.backends():
    config = backend.configuration()
    if not config.simulator:
        status = backend.status()
        print(f"	{backend.name}, Number of Qubits: {config.n_qubits}, Queue length: {status.pending_jobs}")
