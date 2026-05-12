from math import pi, pow
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import Aer


def IQFT(circuit, qin, n):
    for i in range (int(n/2)):
        circuit.swap(qin[i], qin[n -1 -i])
    for i in range (n):
        circuit.h(qin[i])
        for j in range (i +1, n, 1):
            circuit.cp(-pi/ pow(2, j-i), qin[j], qin[i])


def run():
    n = 3
    qin = QuantumRegister(n)
    cr = ClassicalRegister(n)
    circuit = QuantumCircuit(qin, cr, name="Inverse_Quantum_Fourier_Transform")

    circuit.h(qin)
    circuit.z(qin[2])
    circuit.s(qin[1])
    circuit.z(qin[0])
    circuit.t(qin[0])

    IQFT(circuit, qin, n)
    circuit.measure (qin, cr)


    backend = Aer.get_backend("qasm_simulator")
    circuit = transpile(circuit, backend)
    result = backend.run(circuit, shots=500).result()
    counts = result.get_counts(circuit)
    print(counts)

    return counts


if __name__ == '__main__':
    run()