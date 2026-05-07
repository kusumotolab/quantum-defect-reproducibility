from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import sys


def run():
    qc = QuantumCircuit(4, 4)
    for i in range(4):
        qc.h(i)
    qc.cx(3, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    qc.ccx(3, 2, 1)
    qc.cx(1, 2)
    qc.cx(3, 2)
    qc.measure(0, 0)
    qc.measure(1, 1)
    qc.measure(2, 2)
    qc.measure(3, 3)
    backend = Aer.get_backend('qasm_simulator')
    max_shots = 2**13
    qc = transpile(qc, backend)
    job = backend.run(qc, shots=max_shots)
    result = job.result()
    count = result.get_counts()
    plot_histogram(count)
    print(count)

    return count, max_shots

if __name__ == '__main__':
    run()