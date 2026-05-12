from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.circuit.library import EfficientSU2


def run():
    circuit = EfficientSU2(1)
    x = Parameter("x")
    circuit.global_phase = x
    bound_circuit = circuit.assign_parameters({x: 0.001}, inplace=False)
    print(circuit.parameters)
    print(circuit.global_phase)
    
    return circuit.global_phase


if __name__ == '__main__':
    run()