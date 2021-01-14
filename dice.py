#!/usr/bin/env python3

import sys
from qiskit import Aer, ClassicalRegister, QuantumRegister, QuantumCircuit, IBMQ, execute
from qiskit.tools.monitor import job_monitor

def _pending_jobs(backend):
    return backend.status().pending_jobs

def _not_simulator(backend):
    return 'simulator' not in backend.name()

def _has_enough_qubits(backend, n_qubits):
    return backend.configuration().n_qubits >= n_qubits

def best_ibmq_backend(n_qubits):
    """Returns the actual-hardware IBMQ backend with the fewest pending jobs."""
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    return sorted(provider.backends(
        filters=lambda b: _not_simulator(b) and _has_enough_qubits(b, n_qubits)
    ), key=_pending_jobs)[0]

dice = 3
sides = 6

bits = 3  # TODO: Calculate based on `num_sides`.

if sys.argv[0] == "real":
    backend = best_ibmq_backend(n_qubits=bits)
else:
    backend = Aer.get_backend('qasm_simulator')

q = QuantumRegister(3, 'q')
c = ClassicalRegister(3, 'c')
circuit = QuantumCircuit(bits, bits)
circuit.h(q[0])
circuit.h(q[1])
circuit.h(q[2])

circuit.measure(q[0], c[0])
circuit.measure(q[1], c[1])
circuit.measure(q[2], c[2])

circuit.reset(q[0]).c_if(c, 7)
circuit.reset(q[1]).c_if(c, 7)
circuit.reset(q[2]).c_if(c, 7)
circuit.reset(q[0]).c_if(c, 0)
circuit.reset(q[1]).c_if(c, 0)
circuit.reset(q[2]).c_if(c, 0)

circuit.measure(q[0], c[0])
circuit.measure(q[1], c[1])
circuit.measure(q[2], c[2])

circuit.h(q[0]).c_if(c, 0)
circuit.h(q[1]).c_if(c, 0)
circuit.h(q[2]).c_if(c, 0)

circuit.measure(q[0], c[0])
circuit.measure(q[1], c[1])
circuit.measure(q[2], c[2])

# Run the job
job = execute(circuit, backend, shots=1)
job_monitor(job)

# Get the results.
result = job.result()
counts = result.get_counts(circuit)

print(counts)
exit()

#number = int(list(counts.keys())[0], 2)

#circuit = build_circuit(bits)
#numbers = [run(circuit, backend, sides) for _ in range(dice)]
numbers = [number]

print(
    f"{dice}d{sides} =",
    " + ".join(map(str, numbers)),
    "=",
    sum(numbers)
)
