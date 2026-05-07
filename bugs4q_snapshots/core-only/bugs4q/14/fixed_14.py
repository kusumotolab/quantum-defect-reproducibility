from qiskit import Aer, QuantumCircuit

from qiskit.opflow import CircuitSampler, StateFn, Z, Y, I
from qiskit.utils import QuantumInstance
from qiskit.opflow.expectations import PauliExpectation


def run():
    state = QuantumCircuit(2)

    state.h(1)
    state.sdg(1)
    state.cz(0, 1)
    state.h(1)
    print(state)

    obs = (Z ^ I) - 1j * (Y ^ I)
    exp_val = ~StateFn(obs) @ StateFn(state)
    exp_val = PauliExpectation().convert(exp_val).reduce()

    print(exp_val)

    print('Eval ', exp_val.eval())  # = 0+1j
    qasm_val = CircuitSampler(QuantumInstance(Aer.get_backend('qasm_simulator'), shots=100000)).convert(exp_val).eval()
    print('Qasm ', qasm_val)  # = 0 (up to shot noise)
    
    return exp_val.eval(), qasm_val


if __name__ == '__main__':
    run()