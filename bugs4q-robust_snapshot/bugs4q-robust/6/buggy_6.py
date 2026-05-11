from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.circuit.library import XGate


def run():
    qr = QuantumRegister(36, "qr")
    cr = ClassicalRegister(36, 'cr')
    qc = QuantumCircuit(qr, cr)
    for i in range(8, 12):
        qc.h(i)
    gate = XGate().control(num_ctrl_qubits=4, ctrl_state='1111')
    qc.append(gate, [8,9,10,11]+[4])
    qc.barrier()
    for i in range(36):
        qc.measure(i, i)
    qc.draw(output='mpl', filename='out')
    backend_sim = Aer.get_backend('qasm_simulator')
    backend_sim.set_max_qubits(36)
    transpiled = transpile(qc, backend=backend_sim)
    job_sim = backend_sim.run(transpiled, shots=1024)
    result_sim = job_sim.result()
    counts = result_sim.get_counts(qc)
    res = []
    for i in counts.keys():
        res.append(i)
    print(res)


if __name__ == '__main__':
    run()