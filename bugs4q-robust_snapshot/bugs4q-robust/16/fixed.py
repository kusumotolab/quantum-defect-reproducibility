from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit_aer import Aer


def run():
    qr = QuantumRegister(5,'qr')
    cr = ClassicalRegister(5, 'cr')
    ghz = QuantumCircuit(qr, cr)

    ghz.h(qr[0])
    ghz.cx(qr[0],qr[1])
    ghz.cx(qr[1],qr[2])
    ghz.cx(qr[2],qr[3])
    ghz.cx(qr[3],qr[4])
    ghz.barrier(qr)
    ghz.draw()

    sim_backend = Aer.get_backend('statevector_simulator')
    ghz = transpile(ghz, sim_backend)
    sim_result = sim_backend.run(ghz).result()
    print(sim_result.get_statevector(0))

    return sim_result.get_statevector(0).data
    

if __name__ == '__main__':
    run()