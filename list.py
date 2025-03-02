from qiskit_ibm_runtime import QiskitRuntimeService

# Initialize the runtime service (automatically loads saved account)
service = QiskitRuntimeService()

# Get all available backends
backends = service.backends()

print("Available Quantum Simulators:")
for backend in backends:
    config = backend.configuration()
    if config.simulator:
        status = backend.status()
        print(f"Simulator: {backend.name}, Queue length: {status.pending_jobs}")

print("\nAvailable Quantum Computers:")
for backend in backends:
    config = backend.configuration()
    if not config.simulator:
        status = backend.status()
        print(f"Quantum Computer: {backend.name}, Number of Qubits: {config.n_qubits}, Queue length: {status.pending_jobs}")