from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram


def run():
  # Use Aer's qasm_simulator
  simulator = Aer.get_backend('qasm_simulator')

  # Create a Quantum Circuit acting on the q register
  circuit = QuantumCircuit(3, 3)

  # Add a X gate on qubit 0
  circuit.x(0)

  # Add a CX (CNOT) gate on control qubit 0 and target qubit 1
  circuit.cx(0, 1)

  circuit.barrier()
  # Map the quantum measurement to the classical bits
  circuit.measure([0,1,2], [0,1,2])

  # Execute the circuit on the qasm simulator
  circuit = transpile(circuit, simulator)
  job = simulator.run(circuit, shots=1000)

  # Grab results from the job
  result = job.result()

  # Returns counts
  counts = result.get_counts(circuit)
  print("\nTotal count:",counts)

  # Draw the circuit
  circuit.draw()

  return counts

if __name__ == '__main__':
    run()