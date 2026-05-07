from qiskit import *


def run():
    qc = QuantumCircuit(1)
    qc.u1(0.24,0)
    print(qc.decompose())

    return qc.decompose()


if __name__ == '__main__':
    run()