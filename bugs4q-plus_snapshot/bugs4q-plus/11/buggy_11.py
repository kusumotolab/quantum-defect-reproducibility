from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.circuit.library import EfficientSU2


def run():
    circuit = EfficientSU2(1)
    x = Parameter("x")
    circuit.global_phase = x
    circuit.assign_parameters({x: 0.001}, inplace=True)
    print(circuit.parameters)
    print(circuit.global_phase)
    
    return circuit.global_phase


if __name__ == '__main__':
    run()