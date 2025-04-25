"""
Example demonstrating Shor metrics via constructor.

Circuit taken from example at https://github.com/qiskit-community/qiskit-community-tutorials/blob/master/algorithms/deutsch_jozsa.ipynb

"""
import math
import numpy as np
from qward.examples.utils import get_display, create_example_circuit
from qward import Scanner
from qward.metrics import QiskitMetrics, ComplexityMetrics
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

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

def main():
    example_metrics_with_classes()
    example_metrics_with_instances()

if __name__ == "__main__":
    main()