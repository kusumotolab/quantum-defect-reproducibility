
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute


def run():
    # Initialize circuit
    m_qubit = QuantumRegister(1)
    search_register = QuantumRegister(4)
    result_register = ClassicalRegister(4)
    ancillaries = QuantumRegister(3)
    circuit = QuantumCircuit(search_register, result_register, m_qubit, ancillaries)

    # Put M qubit into 1-superposition
    circuit.x(m_qubit)
    circuit.h(m_qubit)

    # Put search qubits into superposition
    circuit.h(search_register)

    # Encode S1 * !S2 * S3
    circuit.x( search_register[2] )
    circuit.ccx( search_register[1], search_register[2], ancillaries[0] )
    circuit.ccx( search_register[3], ancillaries[0], ancillaries[1] )

    # Encode S0 * S1
    circuit.ccx( search_register[0], search_register[1], ancillaries[2] )

    # Encode oracle ((S0 * S1) + (S1 * !S2 * S3))
    circuit.x(ancillaries)
    circuit.ccx( ancillaries[1], ancillaries[2], m_qubit[0] )
    circuit.x(m_qubit)

    # Return ancillaries to 0s so they can be used later
    circuit.x(ancillaries)
    circuit.ccx( search_register[0], search_register[1], ancillaries[2] )
    circuit.ccx( search_register[3], ancillaries[0], ancillaries[1] )
    circuit.ccx( search_register[1], search_register[2], ancillaries[0] )
    circuit.x( search_register[2] )

    # Do rotation about the average (diffusion)
    circuit.h(search_register)
    circuit.x(search_register)

    circuit.h(search_register[3])
    circuit.mcx(search_register[0:3], search_register[3])
    circuit.h(search_register[3])

    circuit.x(search_register)
    circuit.h(search_register)

    circuit.measure(search_register, result_register)

    # Run the circuit with a given number of shots
    backend_sim = Aer.get_backend('qasm_simulator')
    job_sim = execute(circuit, backend_sim, shots = 1024)
    result_sim = job_sim.result()

    # get_counts returns a dictionary with the bit-strings as keys
    # and the number of times the string resulted as the value
    counts = result_sim.get_counts()
    print(counts)

    return counts


if __name__ == '__main__':
    run()