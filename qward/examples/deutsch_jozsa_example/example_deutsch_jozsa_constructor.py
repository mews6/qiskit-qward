"""
Example demonstrating Shor metrics via constructor.

Circuit taken from example at https://github.com/qiskit-community/qiskit-community-tutorials/blob/master/algorithms/deutsch_jozsa.ipynb

"""
import math
import numpy as np
from qward.examples.utils import get_display, create_example_circuit
from qward import Scanner
from qward.metrics import QiskitMetrics, ComplexityMetrics, SuccessRate
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator, AerJob
display = get_display()


def create_example_dj(n):
    # Choose a type of oracle at random. With probability half it is constant, 
    # and with the same probability it is balanced
    oracleType, oracleValue = np.random.randint(2), np.random.randint(2)

    if oracleType == 0:
        print("The oracle returns a constant value ", oracleValue)
    else:
        print("The oracle returns a balanced function")
        a = np.random.randint(1,2**n) # this is a hidden parameter for balanced oracle. 

    # Creating registers
    # n qubits for querying the oracle and one qubit for storing the answer
    qr = QuantumRegister(n+1) #all qubits are initialized to zero
    # for recording the measurement on the first register
    cr = ClassicalRegister(n, name='res')

    circuitName = "DeutschJozsa"
    djCircuit = QuantumCircuit(qr, cr)

    # Create the superposition of all input queries in the first register by applying the Hadamard gate to each qubit.
    for i in range(n):
        djCircuit.h(qr[i])

    # Flip the second register and apply the Hadamard gate.
    djCircuit.x(qr[n])
    djCircuit.h(qr[n])
        
    # Apply barrier to mark the beginning of the oracle
    djCircuit.barrier()

    if oracleType == 0:#If the oracleType is "0", the oracle returns oracleValue for all input. 
        if oracleValue == 1:
            djCircuit.x(qr[n])
        else:
            djCircuit.id(qr[n])
    else: # Otherwise, it returns the inner product of the input with a (non-zero bitstring) 
        for i in range(n):
            if (a & (1 << i)):
                djCircuit.cx(qr[i], qr[n])
            
    # Apply barrier to mark the end of the oracle
    djCircuit.barrier()

    # Apply Hadamard gates after querying the oracle
    for i in range(n):
        djCircuit.h(qr[i])
        
    # Measurement
    djCircuit.barrier()
    for i in range(n):
        djCircuit.measure(qr[i], cr[i])
    return djCircuit

def example_metrics_with_classes():
    circuit = create_example_dj(10)
    print("\nExample: Metrics via Scanner constructor (metric classes)")
    scanner = Scanner(circuit=circuit, metrics=[QiskitMetrics, ComplexityMetrics])
    metrics_dict = scanner.calculate_metrics()
    for metric_name, df in metrics_dict.items():
        print(f"{metric_name} DataFrame:")
        display(df)


def example_metrics_with_instances():
    circuit = create_example_dj(10)
    print("\nExample: Metrics via Scanner constructor (metric instances)")
    qm = QiskitMetrics(circuit)
    cm = ComplexityMetrics(circuit)
    scanner = Scanner(circuit=circuit, metrics=[qm, cm])
    metrics_dict = scanner.calculate_metrics()
    for metric_name, df in metrics_dict.items():
        print(f"{metric_name} DataFrame:")
        display(df)


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

def main():
    example_metrics_with_classes()
    example_metrics_with_instances()
    example_multiple_jobs_success_rate(create_example_dj(10),10)

if __name__ == "__main__":
    main()