from qiskit import *
from qiskit_aer import QasmSimulator
import sys


def run():
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.x(1)
    circuit.cx(0,1)
    circuit.measure_all()

    backend=QasmSimulator()
    max_shots = 2**12
    job_sim=backend.run(transpile(circuit,backend),shots=max_shots)
    result_sim=job_sim.result()

    counts=result_sim.get_counts(circuit)
    print(counts)
    print(circuit)

    return counts, max_shots


if __name__ == '__main__':
    run()