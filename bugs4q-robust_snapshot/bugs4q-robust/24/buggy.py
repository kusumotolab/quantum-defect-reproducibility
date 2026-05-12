import qiskit
from qiskit import *


def run():
    qr = QuantumRegister(2)
    cr = ClassicalRegister(2)
    circuit = QuantumCircuit(qr, cr)
    #%matplotlib inline
    circuit.draw(output='mpl')
    circuit.h(qr(0))


if __name__ == '__main__':
    run()