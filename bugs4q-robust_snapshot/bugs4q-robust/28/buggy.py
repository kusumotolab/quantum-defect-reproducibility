from qiskit import *


def run():
    circuit = QuantumCircuit(1)
    circuit.iden(0)
    print(circuit)


if __name__ == '__main__':
    run()