from qiskit import *
from qiskit import transpile
from qiskit_aer import Aer


def run():
    qubit = QuantumRegister(1, 'qubit')
    circuit = QuantumCircuit(qubit)

    circuit.x(qubit)
    circuit.barrier(qubit)
    circuit.id(qubit)
    circuit.barrier(qubit)
    circuit.rx(3.1416, qubit)

    backend = Aer.get_backend('statevector_simulator')
    circuit = transpile(circuit, backend)
    result = backend.run(circuit).result()
    outputstate = result.get_statevector(circuit, decimals=3)
    print(outputstate)


if __name__ == '__main__':
    run()