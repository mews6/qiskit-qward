"""
Example demonstrating Grover metrics via constructor.
"""
from math import pi, sqrt
import math
from qward.examples.utils import get_display
from qward import Scanner
from qward.metrics import QiskitMetrics, ComplexityMetrics, SuccessRate
from qiskit.quantum_info import DensityMatrix as dm
from qiskit import QuantumRegister as qr
from qiskit import QuantumCircuit as qc
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator, AerJob
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.compiler import transpile

display = get_display()

def example_multiple_jobs_success_rate(circuit: QuantumCircuit, n: int):
    """
    Example 7: Using SuccessRate with multiple Aer simulator jobs

    This example demonstrates how to use SuccessRate with multiple Aer simulator jobs
    to analyze the success rate across different runs.

    Args:
        circuit: The quantum circuit to analyze
    """
    print("\nExample 7: Using SuccessRate with multiple Aer simulator jobs")

    # Import noise model components
    from qiskit_aer.noise import (
        NoiseModel,
        QuantumError,
        ReadoutError,
        pauli_error,
        depolarizing_error,
    )

    # Create an Aer simulator with default settings (no noise)
    simulator = AerSimulator()

    # Run the circuit multiple times with different noise models
    jobs = []

    # Run with default noise model (no noise)
    job1 = simulator.run(circuit, shots=1024)
    jobs.append(job1)

    # Create a noise model with depolarizing errors
    noise_model1 = NoiseModel()

    # Add depolarizing error to all single qubit gates
    depol_error = depolarizing_error(0.05, 1)  # 5% depolarizing error
    noise_model1.add_all_qubit_quantum_error(depol_error, ["u1", "u2", "u3"])

    # Add depolarizing error to all two qubit gates
    depol_error_2q = depolarizing_error(0.1, 2)  # 10% depolarizing error
    noise_model1.add_all_qubit_quantum_error(depol_error_2q, ["cx"])

    # Add readout error
    readout_error = ReadoutError([[0.9, 0.1], [0.1, 0.9]])  # 10% readout error
    noise_model1.add_all_qubit_readout_error(readout_error)

    # Create a simulator with the first noise model
    noisy_simulator1 = AerSimulator(noise_model=noise_model1)
    job2 = noisy_simulator1.run(circuit, shots=1024)
    jobs.append(job2)

    # Create a noise model with Pauli errors
    noise_model2 = NoiseModel()

    # Add Pauli error to all single qubit gates
    pauli_error_1q = pauli_error([("X", 0.05), ("Y", 0.05), ("Z", 0.05), ("I", 0.85)])
    noise_model2.add_all_qubit_quantum_error(pauli_error_1q, ["u1", "u2", "u3"])

    # Add Pauli error to all two qubit gates
    pauli_error_2q = pauli_error([("XX", 0.05), ("YY", 0.05), ("ZZ", 0.05), ("II", 0.85)])
    noise_model2.add_all_qubit_quantum_error(pauli_error_2q, ["cx"])

    # Add readout error
    readout_error = ReadoutError([[0.95, 0.05], [0.05, 0.95]])  # 5% readout error
    noise_model2.add_all_qubit_readout_error(readout_error)

    # Create a simulator with the second noise model
    noisy_simulator2 = AerSimulator(noise_model=noise_model2)
    job3 = noisy_simulator2.run(circuit, shots=1024)
    jobs.append(job3)

    # Wait for all jobs to complete
    for job in jobs:
        job.result()

    # Create a scanner with the circuit
    scanner = Scanner(circuit=circuit)

    # Add SuccessRate metric with multiple jobs
    success_rate_metric = SuccessRate(circuit=circuit, success_criteria=lambda x: x == "11")

    # Add jobs one by one to demonstrate the new functionality
    success_rate_metric.add_job(jobs[0])  # Add first job
    success_rate_metric.add_job(jobs[1:])  # Add remaining jobs as a list

    scanner.add_metric(success_rate_metric)

    # Calculate metrics
    metrics_dict = scanner.calculate_metrics()

    # Display the individual jobs metrics
    print("\nSuccess rate individual jobs DataFrame:")
    display(metrics_dict["SuccessRate.individual_jobs"])

    # Display the aggregate metrics
    print("\nSuccess rate aggregate metrics DataFrame:")
    display(metrics_dict["SuccessRate.aggregate"])

    # Compare individual job results
    print("\nIndividual job results:")
    for i, job in enumerate(jobs):
        result = job.result()
        counts = result.get_counts()
        total_shots = sum(counts.values())
        successful_shots = counts.get('1'*n, 0)
        success_rate = successful_shots / total_shots if total_shots > 0 else 0.0

        print(f"Job {i+1} success rate: {success_rate:.4f}")
        print(f"Job {i+1} counts: {counts}")

    return scanner, jobs

def example_multiple_jobs_success_rate(circuit: QuantumCircuit):
    """
    Example 7: Using SuccessRate with multiple Aer simulator jobs

    This example demonstrates how to use SuccessRate with multiple Aer simulator jobs
    to analyze the success rate across different runs.

    Args:
        circuit: The quantum circuit to analyze
    """
    print("\nExample 7: Using SuccessRate with multiple Aer simulator jobs")

    # Import noise model components
    from qiskit_aer.noise import (
        NoiseModel,
        QuantumError,
        ReadoutError,
        pauli_error,
        depolarizing_error,
    )

    # Create an Aer simulator with default settings (no noise)
    simulator = AerSimulator()

    # Run the circuit multiple times with different noise models
    jobs = []

    # Run with default noise model (no noise)
    job1 = simulator.run(circuit, shots=1024)
    jobs.append(job1)

    # Create a noise model with depolarizing errors
    noise_model1 = NoiseModel()

    # Add depolarizing error to all single qubit gates
    depol_error = depolarizing_error(0.05, 1)  # 5% depolarizing error
    noise_model1.add_all_qubit_quantum_error(depol_error, ["u1", "u2", "u3"])

    # Add depolarizing error to all two qubit gates
    depol_error_2q = depolarizing_error(0.1, 2)  # 10% depolarizing error
    noise_model1.add_all_qubit_quantum_error(depol_error_2q, ["cx"])

    # Add readout error
    readout_error = ReadoutError([[0.9, 0.1], [0.1, 0.9]])  # 10% readout error
    noise_model1.add_all_qubit_readout_error(readout_error)

    # Create a simulator with the first noise model
    noisy_simulator1 = AerSimulator(noise_model=noise_model1)
    job2 = noisy_simulator1.run(circuit, shots=1024)
    jobs.append(job2)

    # Create a noise model with Pauli errors
    noise_model2 = NoiseModel()

    # Add Pauli error to all single qubit gates
    pauli_error_1q = pauli_error([("X", 0.05), ("Y", 0.05), ("Z", 0.05), ("I", 0.85)])
    noise_model2.add_all_qubit_quantum_error(pauli_error_1q, ["u1", "u2", "u3"])

    # Add Pauli error to all two qubit gates
    pauli_error_2q = pauli_error([("XX", 0.05), ("YY", 0.05), ("ZZ", 0.05), ("II", 0.85)])
    noise_model2.add_all_qubit_quantum_error(pauli_error_2q, ["cx"])

    # Add readout error
    readout_error = ReadoutError([[0.95, 0.05], [0.05, 0.95]])  # 5% readout error
    noise_model2.add_all_qubit_readout_error(readout_error)

    # Create a simulator with the second noise model
    noisy_simulator2 = AerSimulator(noise_model=noise_model2)
    job3 = noisy_simulator2.run(circuit, shots=1024)
    jobs.append(job3)

    # Wait for all jobs to complete
    for job in jobs:
        job.result()

    # Create a scanner with the circuit
    scanner = Scanner(circuit=circuit)

    # Add SuccessRate metric with multiple jobs
    success_rate_metric = SuccessRate(circuit=circuit, success_criteria=lambda x: x == "11")

    # Add jobs one by one to demonstrate the new functionality
    success_rate_metric.add_job(jobs[0])  # Add first job
    success_rate_metric.add_job(jobs[1:])  # Add remaining jobs as a list

    scanner.add_metric(success_rate_metric)

    # Calculate metrics
    metrics_dict = scanner.calculate_metrics()

    # Display the individual jobs metrics
    print("\nSuccess rate individual jobs DataFrame:")
    display(metrics_dict["SuccessRate.individual_jobs"])

    # Display the aggregate metrics
    print("\nSuccess rate aggregate metrics DataFrame:")
    display(metrics_dict["SuccessRate.aggregate"])

    # Compare individual job results
    print("\nIndividual job results:")
    for i, job in enumerate(jobs):
        result = job.result()
        counts = result.get_counts()
        total_shots = sum(counts.values())
        successful_shots = counts.get('1111', 0)
        success_rate = successful_shots / total_shots if total_shots > 0 else 0.0

        print(f"Job {i+1} success rate: {success_rate:.4f}")
        print(f"Job {i+1} counts: {counts}")

    return scanner, jobs

def create_oracle(marked_states):
    """Build a Grover oracle for multiple marked states

    Here we assume all input marked states have the same number of bits

    Parameters:
        marked_states (str or list): Marked states of oracle

    Returns:
        QuantumCircuit: Quantum circuit representing Grover oracle
    """
    if not isinstance(marked_states, list):
        marked_states = [marked_states]
    # Compute the number of qubits in circuit
    num_qubits = len(marked_states[0])

    qc = QuantumCircuit(num_qubits)
    # Mark each target state in the input list
    for target in marked_states:
        # Flip target bit-string to match Qiskit bit-ordering
        rev_target = target[::-1]
        # Find the indices of all the '0' elements in bit-string
        zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("1", ind)]
        # Add a multi-controlled Z-gate with pre- and post-applied X-gates (open-controls)
        # where the target bit-string has a '0' entry
        qc.x(zero_inds)
        qc.compose(MCMT(ZGate(), num_qubits - 1, 1).decompose(), inplace=True)
        qc.x(zero_inds)
    return qc

def create_example_grover():

    optimal_num_iterations = math.floor(
        math.pi / (4 * math.asin(math.sqrt(1 / 2**4)))
    )
    
    oracle = create_oracle(["1111"])
    grover_op = GroverOperator(oracle)
    qc = QuantumCircuit(grover_op.num_qubits)
    # Create even superposition of all basis states
    qc.h(range(grover_op.num_qubits))
    # Apply Grover operator the optimal number of times
    qc.compose(grover_op.power(optimal_num_iterations).decompose(), inplace=True)
    # Measure all qubits
    qc.measure_all()
    
    return qc.decompose()
 
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
    create_example_grover()
    example_multiple_jobs_success_rate(create_example_grover())

if __name__ == "__main__":
    main()