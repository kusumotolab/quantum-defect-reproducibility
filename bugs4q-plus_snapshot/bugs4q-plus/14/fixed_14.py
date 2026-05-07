import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit.primitives import BackendEstimatorV2
from qiskit_aer import AerSimulator


def run():
    state = QuantumCircuit(2)
    state.h(1)
    state.sdg(1)
    state.cz(0, 1)
    state.h(1)
    print(state)

    obs = SparsePauliOp(["ZI", "YI"], coeffs=[1.0, -1j])
    obs_meas = obs.adjoint()

    sv = Statevector.from_instruction(state)
    exact_val = sv.expectation_value(obs_meas)
    print("Eval ", exact_val)

    max_shots = 2**13
    paulis = SparsePauliOp(obs_meas.paulis)
    coeffs = obs_meas.coeffs

    estimator = BackendEstimatorV2(
        backend=AerSimulator(),
        options={"default_precision": 1.0 / np.sqrt(max_shots)},
    )
    job = estimator.run([(state, list(paulis))])
    evs = np.asarray(job.result()[0].data.evs)
    qasm_val = complex(np.dot(coeffs, evs))
    print("Qasm ", qasm_val)

    return exact_val, qasm_val, max_shots


if __name__ == "__main__":
    run()