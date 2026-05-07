from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector


def apply_oracle(circuit, search_register, m_qubit, ancillaries):
    # Encode S1 * !S2 * S3
    circuit.x(search_register[2])
    circuit.ccx(search_register[1], search_register[2], ancillaries[0])
    circuit.ccx(search_register[3], ancillaries[0], ancillaries[1])

    # Encode S0 * S1
    circuit.ccx(search_register[0], search_register[1], ancillaries[2])

    # Encode oracle
    circuit.x(ancillaries)
    circuit.ccx(ancillaries[1], ancillaries[2], m_qubit[0])
    circuit.x(m_qubit)

    # Uncompute
    circuit.x(ancillaries)
    circuit.ccx(search_register[0], search_register[1], ancillaries[2])
    circuit.ccx(search_register[3], ancillaries[0], ancillaries[1])
    circuit.ccx(search_register[1], search_register[2], ancillaries[0])
    circuit.x(search_register[2])


def oracle_phase_table():
    marked = []
    unmarked = []

    for x in range(16):
        search = QuantumRegister(4, "s")
        m = QuantumRegister(1, "m")
        anc = QuantumRegister(3, "a")
        qc = QuantumCircuit(search, m, anc)

        bits = format(x, "04b")
        for i, b in enumerate(bits):
            if b == "1":
                qc.x(search[i])

        # m_qubit = |->
        qc.x(m[0])
        qc.h(m[0])

        apply_oracle(qc, search, m, anc)

        sv = Statevector.from_instruction(qc)
        nz = [(k, v) for k, v in sv.to_dict().items() if abs(v) > 1e-9]

        if len(nz) != 2:
            print(f"x={bits}: unexpected number of components")
            for basis, amp in nz:
                print("   ", basis, amp)
            continue

        # 実数符号だけ見る
        amps = [amp.real for _, amp in nz]
        signs = tuple(1 if a > 0 else -1 for a in amps)

        print(f"x={bits}: {nz[0][0]} {amps[0]: .3f}, {nz[1][0]} {amps[1]: .3f}")

        if signs == (1, -1):
            unmarked.append(bits)
        elif signs == (-1, 1):
            marked.append(bits)
        else:
            print(f"x={bits}: unexpected sign pattern {signs}")

    print("\nMarked states:", marked)
    print("Unmarked states:", unmarked)


if __name__ == "__main__":
    oracle_phase_table()