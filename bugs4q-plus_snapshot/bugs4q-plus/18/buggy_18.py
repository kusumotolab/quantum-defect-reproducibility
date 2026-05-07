from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer


def run():
    backend = Aer.get_backend('statevector_simulator')
    qc = QuantumCircuit(2, 2)
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0,1], [0,1])
    qc = transpile(qc, backend)
    result = backend.run(qc, 100).result()
    print(result.get_counts(qc))


if __name__ == '__main__':
    run()