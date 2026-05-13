from qiskit import QuantumCircuit
from qiskit_experiments.library import ProcessTomography
from qiskit_experiments.library.tomography.basis import (
    Pauli6PreparationBasis,
    PauliMeasurementBasis,
    PauliPreparationBasis,
)
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeParisV2


def raise_if_analysis_failed(experiment):
    status = experiment.analysis_status()
    status_name = status.name if hasattr(status, "name") else str(status)
    if status_name == "ERROR":
        raise RuntimeError(f"Qiskit Experiments analysis failed: {status}")



def run():
    backend = AerSimulator.from_backend(FakeParisV2())

    circ = QuantumCircuit(1,1)
    circ.x(0)

    # or       tomo = ProcessTomography(circuit=circ)
    tomo = ProcessTomography(                   
        circuit=circ,
        measurement_basis=PauliMeasurementBasis(),
        preparation_basis=PauliPreparationBasis(),
        basis_indices=None,
    )


    print(f"There are {len(tomo.circuits())} circuits to run")

    # This works
    experiment = tomo.run(analysis=False, backend=backend).block_for_results()
    raise_if_analysis_failed(experiment)

    # This doesn't
    experiment = tomo.run(analysis=True, backend=backend).block_for_results()
    raise_if_analysis_failed(experiment)
    

if __name__ == '__main__':
    run()