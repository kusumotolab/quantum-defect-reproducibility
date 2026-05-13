from qiskit import QuantumCircuit, transpile


def run():
    qc = QuantumCircuit(1)
    qc.p(0.24, 0)
    print(qc.decompose())

    return qc.decompose()


if __name__ == '__main__':
    run()