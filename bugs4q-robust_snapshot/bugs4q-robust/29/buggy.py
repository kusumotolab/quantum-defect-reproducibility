from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
import math
from qiskit_aer import Aer


def qft_dagger(circ, q, n):
    for i in range(n-1,-1,-1):
        for m in range(n-i,1,-1):
            circ.cp(-2*math.pi/2**m, q[i+m-1], q[i])
        circ.h(q[i])
        circ.barrier()


def n_hadamard(circ, q, n):
    for i in range(n):
        circ.h(q[i])


def build_state_vector(circ, inp, s):
    for i, e in enumerate(inp):
        if e == '1':
            circ.x(s[i])


def run():
    nancilla = 3
    theta = 0.78
    q = QuantumRegister(nancilla, 'q')
    s = QuantumRegister(1, 's')
    c = ClassicalRegister(nancilla, 'c')

    qpe = QuantumCircuit(q, s, c)

    build_state_vector(qpe, '1', s)
    n_hadamard(qpe, q, nancilla)

    for i in range(nancilla):
        qpe.cp(2*math.pi*theta*2**(nancilla-i-1), q[i], s[0])

    qft_dagger(qpe, q, nancilla)

    for i in range(nancilla):
        qpe.measure(q[i],c[i])

    backend = Aer.get_backend('qasm_simulator')
    qpe = transpile(qpe, backend)
    results = backend.run(qpe, shots=1000).result()
    answer = results.get_counts()
    print(answer)

    return answer


if __name__ == '__main__':
    run()