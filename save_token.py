from qiskit_ibm_runtime import QiskitRuntimeService

# Replace "YOUR_API_TOKEN" by your actual IBMQ token 
QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_API_TOKEN", overwrite = True)