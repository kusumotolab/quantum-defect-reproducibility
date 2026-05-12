import numpy as np
from qiskit.circuit.library import real_amplitudes
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms.gradients import (
    ParamShiftSamplerGradient,
    FiniteDiffSamplerGradient,
    LinCombSamplerGradient,
)

GRADIENTS = {
    "param_shift": lambda s: ParamShiftSamplerGradient(sampler=s),
    "fin_diff":    lambda s: FiniteDiffSamplerGradient(sampler=s, epsilon=1e-6),
    "lin_comb":    lambda s: LinCombSamplerGradient(sampler=s),
}


def run():
    ansatz = real_amplitudes(num_qubits=1, reps=1).decompose()
    circ = ansatz.copy()
    circ.measure_all()

    sampler = StatevectorSampler()
    values = np.random.rand(ansatz.num_parameters)

    for method, make_grad in GRADIENTS.items():
        grad = make_grad(sampler)
        grad.run(circuits=[circ], parameter_values=[values]).result()
        print(f"{method} is ok")


if __name__ == "__main__":
    run()