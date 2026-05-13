from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit_aer.library import *


def run():
    q1 = QuantumCircuit(2)
    q1.save_statevector() # Save initial state
    q1.h(0)
    q1.save_statevector() # Save state after Hadamard
    q1.cx(0, 1)
    q1.save_statevector() # Save state after CNOT (also a final state)
    backend = Aer.get_backend('aer_simulator')
    q1 = transpile(q1, backend)
    job = backend.run(q1, shots=1024)
    statevectors = job.result().get_statevector()


if __name__ == '__main__':
    run()