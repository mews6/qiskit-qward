"""
Example demonstrating Grover metrics via constructor.
"""
from math import pi, sqrt
from qward.examples.utils import get_display
from qward import Scanner
from qward.metrics import QiskitMetrics, ComplexityMetrics
from qiskit.quantum_info import DensityMatrix as dm
from qiskit import QuantumRegister as qr
from qiskit import QuantumCircuit as qc

display = get_display()

"""Number of qubits."""
N: int = 4

"""How much optimization to perform on the circuits.
   Higher levels are more optimized, but take longer to transpile.

   * 0 = No optimization
   * 1 = Light optimization
   * 2 = Heavy optimization
   * 3 = Heavier optimization
"""
OPTIMIZATION_LEVEL: int = 2

"""Set of m nonnegative integers to search for using Grover's algorithm (i.e. TARGETS in base 10)."""
SEARCH_VALUES: set[int] = { 9, 0, 3 }

"""Amount of times to simulate the algorithm."""
SHOTS: int = 10000

"""Set of m N-qubit binary strings representing target state(s) (i.e. SEARCH_VALUES in base 2)."""
TARGETS: set[str] = { f"{s:0{N}b}" for s in SEARCH_VALUES }

"""N-qubit quantum register."""
QUBITS: qr = qr(N, "qubit")

def flip(target: str, qc: qc, qubit: str = "0") -> None:
    """Flips qubit in target state.

    Args:
        target (str): Binary string representing target state.
        qc (qc): Quantum circuit.
        qubit (str, optional): Qubit to flip. Defaults to "0".
    """
    for i in range(len(target)):
        if target[i] == qubit:
            qc.x(i) # Pauli-X gate
            
def oracle(targets: set[str] = TARGETS, name: str = "Oracle") -> qc:
    """Mark target state(s) with negative phase.

    Args:
        targets (set[str]): Binary string(s) representing target state(s). Defaults to TARGETS.
        name (str, optional): Quantum circuit's name. Defaults to "Oracle".

    Returns:
        qc: Quantum circuit representation of oracle.
    """
    # Create N-qubit quantum circuit for oracle
    oracle = qc(QUBITS, name = name)

    for target in targets:
        # Reverse target state since Qiskit uses little-endian for qubit ordering
        target = target[::-1]
        
        # Flip zero qubits in target
        flip(target, oracle, "0")

        # Simulate (N - 1)-control Z gate
        oracle.h(N - 1)                       # Hadamard gate
        oracle.mcx(list(range(N - 1)), N - 1) # (N - 1)-control Toffoli gate
        oracle.h(N - 1)                       # Hadamard gate

        # Flip back to original state
        flip(target, oracle, "0")

    return oracle

def diffuser(name: str = "Diffuser") -> qc:
    """Amplify target state(s) amplitude, which decreases the amplitudes of other states
    and increases the probability of getting the correct solution (i.e. target state(s)).

    Args:
        name (str, optional): Quantum circuit's name. Defaults to "Diffuser".

    Returns:
        qc: Quantum circuit representation of diffuser (i.e. Grover's diffusion operator).
    """
    # Create N-qubit quantum circuit for diffuser
    diffuser = qc(QUBITS, name = name)
    
    diffuser.h(QUBITS)                                    # Hadamard gate
    diffuser.append(oracle({ "0" * N }), list(range(N)))  # Oracle with all zero target state
    diffuser.h(QUBITS)                                    # Hadamard gate
    
    return diffuser

def grover(oracle: qc = oracle(), diffuser: qc = diffuser(), name: str = "Grover Circuit") -> tuple[qc, dm]:
    """Create quantum circuit representation of Grover's algorithm,
    which consists of 4 parts: (1) state preparation/initialization,
    (2) oracle, (3) diffuser, and (4) measurement of resulting state.
    
    Steps 2-3 are repeated an optimal number of times (i.e. Grover's
    iterate) in order to maximize probability of success of Grover's algorithm.

    Args:
        oracle (qc, optional): Quantum circuit representation of oracle. Defaults to oracle().
        diffuser (qc, optional): Quantum circuit representation of diffuser. Defaults to diffuser().
        name (str, optional): Quantum circuit's name. Defaults to "Grover Circuit".

    Returns:
        tuple[qc, dm]: Quantum circuit representation of Grover's algorithm and its density matrix.
    """
    # Create N-qubit quantum circuit for Grover's algorithm
    grover = qc(QUBITS, name = name)

    # Intialize qubits with Hadamard gate (i.e. uniform superposition)
    grover.h(QUBITS)
    
    # Apply barrier to separate steps
    grover.barrier()
    
    # Apply oracle and diffuser (i.e. Grover operator) optimal number of times
    for _ in range(int((pi / 4) * sqrt((2 ** N) / len(TARGETS)))):
        grover.append(oracle, list(range(N)))
        grover.append(diffuser, list(range(N)))

    # Generate density matrix representation of Grover's algorithm
    density_matrix = dm(grover)

    # Measure all qubits once finished
    grover.measure_all()
    
    return grover, density_matrix

def create_example_grover():
    grover_oracle = oracle()
    grover_diffuser = diffuser()

    grover_circuit, density_matrix = grover(grover_oracle, grover_diffuser)
    return grover_circuit

def example_metrics_with_classes():
    circuit = create_example_grover()
    print("\nExample: Metrics via Scanner constructor (metric classes)")
    scanner = Scanner(circuit=circuit, metrics=[QiskitMetrics, ComplexityMetrics])
    metrics_dict = scanner.calculate_metrics()
    for metric_name, df in metrics_dict.items():
        print(f"{metric_name} DataFrame:")
        display(df)


def example_metrics_with_instances():
    circuit = create_example_grover()
    print("\nExample: Metrics via Scanner constructor (metric instances)")
    qm = QiskitMetrics(circuit)
    cm = ComplexityMetrics(circuit)
    scanner = Scanner(circuit=circuit, metrics=[qm, cm])
    metrics_dict = scanner.calculate_metrics()
    for metric_name, df in metrics_dict.items():
        print(f"{metric_name} DataFrame:")
        display(df)

def main():
    example_metrics_with_classes()
    example_metrics_with_instances()

if __name__ == "__main__":
    main()