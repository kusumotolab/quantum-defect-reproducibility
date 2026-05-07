from qiskit import *
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import Aer
from qiskit.compiler import transpile

def run():
    n_qubits = 5
    qc_list = []

    for i in range(n_qubits):
        qr = QuantumRegister(n_qubits)
        cr = ClassicalRegister(n_qubits)
        qc = QuantumCircuit(qr, cr)
        qc.x(qr[i])
        qc.measure(qr, cr)
        qc_list.append(qc)

    backend = Aer.get_backend('qasm_simulator')
    transpiled_circs = transpile(qc_list, backend=backend)
    job_info = backend.run(transpiled_circs)
    for circ_index in range(len(transpiled_circs)):
        print(job_info.result().get_counts(transpiled_circs[circ_index]))


if __name__ == '__main__':
    run()