from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit_aer import Aer
import sys


def run():
    qr = QuantumRegister(2, name='qreg')
    cr = ClassicalRegister(2, name='creg')
    qc = QuantumCircuit(qr,cr)
    qc.h(qr)
    qc.measure_all()

    bkd = Aer.get_backend('qasm_simulator')
    max_shots = 2**13
    new_circuit = transpile(qc, backend = bkd)
    res = bkd.run(new_circuit, shots=max_shots).result()
    print(res.get_counts())
    
    return res.get_counts(), max_shots


if __name__ == '__main__':
    run()