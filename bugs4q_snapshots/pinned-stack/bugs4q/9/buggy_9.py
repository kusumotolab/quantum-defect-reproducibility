from qiskit.circuit import Parameter
from qiskit import pulse
from qiskit.test.mock.backends.almaden import *


def run():
    phase = Parameter('phase')

    with pulse.build(FakeAlmaden()) as phase_test_sched:
        pulse.ShiftPhase(phase, pulse.drive_channel(0))

        phase_test_sched.instructions # ()
        
    return phase_test_sched.instructions # ()


if __name__ == '__main__':
    run()