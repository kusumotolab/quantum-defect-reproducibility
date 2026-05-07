from qiskit import *
from qiskit.extensions import HGate, CXGate
import qiskit.quantum_info as qi


def run():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0,1)

    qc.draw('mpl')
    # no issues with the below line
    qi.Operator.from_label('H') 
    qi.Operator.from_label('X')


if __name__ == '__main__':
    run()