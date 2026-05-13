from qiskit.circuit import Parameter
from qiskit import pulse
from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2


def run():
    phase = Parameter('phase')

    with pulse.build(FakeAlmadenV2()) as phase_test_sched:
        pulse.ShiftPhase(phase, pulse.drive_channel(0))

        phase_test_sched.instructions # ()
        
    return phase_test_sched.instructions # ()


if __name__ == '__main__':
    run()