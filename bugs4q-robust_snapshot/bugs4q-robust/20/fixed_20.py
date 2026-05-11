import qiskit as qk
from qiskit import transpile
from qiskit_aer import Aer


def run():
    my_backend = Aer.get_backend("qasm_simulator")
    qr = qk.QuantumRegister(2)
    cr = qk.ClassicalRegister(2)
    qc = qk.QuantumCircuit(qr,cr)
    print(qc.h(qr[0]))
    measure_Z = qk.QuantumCircuit(qr,cr)
    print(measure_Z.measure(qr,cr))
    measure_X = qk.QuantumCircuit(qr,cr)
    test_Z = qc.compose(measure_Z)
    test_X = qc.compose(measure_X)
    test_Z = transpile(test_Z, backend=my_backend)
    test_X = transpile(test_X, backend=my_backend)
    job_1 = my_backend.run([test_Z, test_X], shots=1000)
    result_1 = job_1.result()
    result_1.get_counts(test_Z)


if __name__ == '__main__':
    run()