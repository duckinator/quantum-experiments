#!/usr/bin/env python3

import numpy as np
from qiskit import Aer, QuantumCircuit, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


qasm_simulator = Aer.get_backend('qasm_simulator')

# Create a Quantum Circuit with 2 qubits and 2 cbits.
circuit = QuantumCircuit(2, 2)

circuit.h(0)        # add h gate on qubit 1
circuit.cx(0, 1)    # add CX/CNOT gate on control qubit 0 and target qubit 1.

# Map the quantum measurement to the classical bits
circuit.measure([0, 1], [0, 1])

job = execute(circuit, qasm_simulator, shots=1000)

result = job.result()
counts = result.get_counts(circuit)

print("\nTotal count for 00 and 11 are:", counts)

# Draw the circuit
circuit.draw(output='mpl')
plot_histogram(counts)
plt.show()
