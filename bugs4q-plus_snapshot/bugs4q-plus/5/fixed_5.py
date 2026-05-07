from qiskit import QuantumCircuit
from qiskit.qasm2 import dumps


def run():
    qasm = '''OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
measure q -> c;'''
    qc = QuantumCircuit.from_qasm_str(qasm)
    print(dumps(qc))

    return dumps(qc)


if __name__ == '__main__':
    run()