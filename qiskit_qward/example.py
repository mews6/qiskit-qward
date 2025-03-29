from qiskit_qward.validators.teleportation_validator import TeleportationValidator
# Comment out the experiments import as it might not exist yet
# from qiskit_qward.experiments.experiments import Experiments
import numpy as np


def main():
    # Create a teleportation validator
    validator = TeleportationValidator(
        payload_size=3,
        gates=["h", "x"],  # Apply Hadamard and X gates to the payload qubit
        use_barriers=True,
    )

    # Create experiments framework - commented out since it might not exist yet
    # experiments = Experiments()

    # Just show the validator features that are available
    print("Teleportation Circuit:")
    print(f"Circuit depth: {validator.depth()}")
    print(f"Operation count: {validator.count_ops()}")
    
    # Run simulation if available
    try:
        print("\nRunning simulation...")
        results = validator.run_simulation()
        print(f"Simulation results: {results}")
    except Exception as e:
        print(f"Simulation error: {e}")

    # Use Qiskit features directly
    validator.draw()  # Draw the circuit


if __name__ == "__main__":
    main()
