from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.visualization import circuit_drawer


def run():
    #definitions
    c = [ ClassicalRegister(1) for _ in range(2) ]
    q = QuantumRegister(1)
    qc = QuantumCircuit(q)
    for register in c:
        qc.add_register( register )
        qc.h(q)
    qc.measure(q,c[0])
    with qc.if_test((c[0], 0)):
        qc.x(q[0])
    qc.measure(q,c[1])
    circuit_drawer(qc)


if __name__ == '__main__':
    run()