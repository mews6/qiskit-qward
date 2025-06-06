"""
Example demonstrating how to use QWARD with Aer simulator.
"""

from qward.examples.utils import get_display, create_example_circuit

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator, AerJob
from qward import Scanner, Result
from qward.metrics import QiskitMetrics, ComplexityMetrics, SuccessRate

display = get_display()


def example_default_metrics(circuit: QuantumCircuit):
    """
    Example 1: Using default metrics (QISKIT and COMPLEXITY)

    This example demonstrates how to use the default metrics provided by QWARD.
    The default metrics include QISKIT and COMPLEXITY metrics.

    Args:
        circuit: The quantum circuit to analyze
    """
    print("\nExample 1: Using default metrics")

    # Create a scanner with the circuit
    scanner = Scanner(circuit=circuit)

    # Add default metrics
    scanner.add_metric(QiskitMetrics(circuit))
    scanner.add_metric(ComplexityMetrics(circuit))

    # Calculate metrics
    metrics_dict = scanner.calculate_metrics()

    # Display each metric DataFrame
    for metric_name, df in metrics_dict.items():
        print(f"\n{metric_name} DataFrame:")
        display(df)

    return scanner


def example_qiskit_metrics(circuit: QuantumCircuit):
    """
    Example 2: Using only QISKIT metrics

    This example demonstrates how to use only QISKIT metrics by creating a QiskitMetrics
    instance and adding it to the Scanner.

    Args:
        circuit: The quantum circuit to analyze
    """
    print("\nExample 2: Using only QISKIT metrics")

    # Create a scanner with the circuit
    scanner = Scanner(circuit=circuit)

    # Add only QiskitMetrics
    scanner.add_metric(QiskitMetrics(circuit))

    # Calculate metrics
    metrics_dict = scanner.calculate_metrics()

    # Display the metrics
    print("Qiskit metrics DataFrame:")
    display(metrics_dict["QiskitMetrics"])

    return scanner


def example_complexity_metrics(circuit: QuantumCircuit):
    """
    Example 3: Using only COMPLEXITY metrics

    This example demonstrates how to use only COMPLEXITY metrics by creating a ComplexityMetrics
    instance and adding it to the Scanner.

    Args:
        circuit: The quantum circuit to analyze
    """
    print("\nExample 3: Using only COMPLEXITY metrics")

    # Create a scanner with the circuit
    scanner = Scanner(circuit=circuit)

    # Add only ComplexityMetrics
    scanner.add_metric(ComplexityMetrics(circuit))

    # Calculate metrics
    metrics_dict = scanner.calculate_metrics()

    # Display the metrics
    print("Complexity metrics DataFrame:")
    display(metrics_dict["ComplexityMetrics"])

    return scanner


def example_multiple_metrics(circuit: QuantumCircuit):
    """
    Example 4: Using multiple metric instances

    This example demonstrates how to use multiple metric instances together by creating
    QiskitMetrics and ComplexityMetrics instances and adding them to the Scanner.

    Args:
        circuit: The quantum circuit to analyze
    """
    print("\nExample 4: Using multiple metric instances")

    # Create a scanner with the circuit
    scanner = Scanner(circuit=circuit)

    # Add multiple metrics
    scanner.add_metric(QiskitMetrics(circuit))
    scanner.add_metric(ComplexityMetrics(circuit))

    # Calculate metrics
    metrics_dict = scanner.calculate_metrics()

    # Display each metric DataFrame
    for metric_name, df in metrics_dict.items():
        print(f"\n{metric_name} DataFrame:")
        display(df)

    return scanner


def example_success_rate_metrics(circuit: QuantumCircuit):
    """
    Example 5: Using SuccessRate with Aer simulator

    This example demonstrates how to use SuccessRate with the Aer simulator.

    Args:
        circuit: The quantum circuit to analyze
    """
    print("\nExample 5: Using SuccessRate with Aer simulator")

    # Create an Aer simulator
    simulator = AerSimulator()

    # Run the circuit
    job = simulator.run(circuit, shots=1024)

    # Get the result
    result = job.result()

    print("Job result:")
    print(result)

    # Create a Result object with the counts from the job result
    counts = result.get_counts()
    qward_result = Result(job=job, counts=counts)

    print("counts:")
    print(counts)
    print("QWARD result:")
    print(qward_result)

    # Create a scanner with the circuit and result
    scanner = Scanner(circuit=circuit, result=qward_result)

    # Add SuccessRate metric
    scanner.add_metric(SuccessRate(circuit=circuit, job=job, success_criteria=lambda x: x == "11"))

    # Calculate metrics
    metrics_dict = scanner.calculate_metrics()

    # Display both individual and aggregate metrics
    print("\nSuccess rate individual jobs DataFrame:")
    display(metrics_dict["SuccessRate.individual_jobs"])

    print("\nSuccess rate aggregate metrics DataFrame:")
    display(metrics_dict["SuccessRate.aggregate"])

    return scanner, job


def example_all_metrics(circuit: QuantumCircuit, job: AerJob):
    """
    Example 6: Using all metrics together

    This example demonstrates how to use all metrics together by creating QiskitMetrics,
    ComplexityMetrics, and SuccessRate instances and adding them to the Scanner.

    Args:
        circuit: The quantum circuit to analyze
        job: The Aer job from the simulator
    """
    print("\nExample 6: Using all metrics together")

    # Get the result
    result = job.result()

    # Create a Result object with the counts from the job result
    counts = result.get_counts()
    qward_result = Result(job=job, counts=counts)

    # Create a scanner with the circuit and result
    scanner = Scanner(circuit=circuit, result=qward_result)

    # Add all metrics
    scanner.add_metric(QiskitMetrics(circuit))
    scanner.add_metric(ComplexityMetrics(circuit))
    scanner.add_metric(SuccessRate(circuit=circuit, job=job, success_criteria=lambda x: x == "11"))

    # Calculate metrics
    metrics_dict = scanner.calculate_metrics()

    # Display each metric DataFrame
    for metric_name, df in metrics_dict.items():
        # Skip SuccessRate metrics as we'll handle them separately
        if not metric_name.startswith("SuccessRate"):
            print(f"\n{metric_name} DataFrame:")
            display(df)

    # Display SuccessRate metrics separately
    if "SuccessRate.individual_jobs" in metrics_dict:
        print("\nSuccessRate Individual Jobs DataFrame:")
        display(metrics_dict["SuccessRate.individual_jobs"])

    if "SuccessRate.aggregate" in metrics_dict:
        print("\nSuccessRate Aggregate Metrics DataFrame:")
        display(metrics_dict["SuccessRate.aggregate"])

    return scanner


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
        successful_shots = counts.get("11", 0)
        success_rate = successful_shots / total_shots if total_shots > 0 else 0.0

        print(f"Job {i+1} success rate: {success_rate:.4f}")
        print(f"Job {i+1} counts: {counts}")

    return scanner, jobs


def main():
    """
    Main function demonstrating how to use QWARD with Aer simulator.
    """
    # Create a simple quantum circuit
    circuit = create_example_circuit()

    # Run the examples
    example_default_metrics(circuit)
    example_qiskit_metrics(circuit)
    example_complexity_metrics(circuit)
    example_multiple_metrics(circuit)

    # Run success rate examples
    _, job = example_success_rate_metrics(circuit)
    example_all_metrics(circuit, job)

    # Run multiple jobs success rate example
    example_multiple_jobs_success_rate(circuit)


if __name__ == "__main__":
    main()
