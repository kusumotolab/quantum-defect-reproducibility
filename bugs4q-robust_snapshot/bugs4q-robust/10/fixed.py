from qiskit import QuantumCircuit, transpile


def run():
    qc = QuantumCircuit(1)
    qc.p(0.24, 0)
    qc = transpile(qc, basis_gates=['p', 'sx', 'rz', 'cx'])
    print(qc)

    return qc


if __name__ == '__main__':
    run()