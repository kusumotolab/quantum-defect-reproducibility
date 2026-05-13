from qiskit import QuantumCircuit


def run():
    qc = QuantumCircuit(3)
    qc.cx(0, 1, label='Label', ctrl_state=0)
    qc.ccx(0, 1, 2, label='Label', ctrl_state=1)


if __name__ == '__main__':
    run()