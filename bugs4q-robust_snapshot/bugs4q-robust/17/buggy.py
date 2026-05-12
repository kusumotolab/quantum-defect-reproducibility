from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import QasmSimulator


def run():
    n = 3
    q = QuantumRegister(n)
    c = ClassicalRegister(n)
    qc = QuantumCircuit(q, c, name="circuit")
    qc.x(0)
    qc.measure([1, 0, 2], [1, 0, 2])
    BACKEND_OPTS_SV = {"method": "statevector"}
    backend = QasmSimulator(**BACKEND_OPTS_SV)
    transpiled = transpile(qc, backend)
    res_SV = backend.run(transpiled, shots=1).result()
    print("counts = " + str(res_SV.get_counts()))

    return res_SV.get_counts()


if __name__ == '__main__':
    run()