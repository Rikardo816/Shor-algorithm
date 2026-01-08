"""
Shor's Algorithm Implementation using Qiskit
This module implements Shor's algorithm for integer factorization on quantum computers.
"""

import math
import random
from fractions import Fraction
from typing import Optional, List, Tuple

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Session


def gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor."""
    while b:
        a, b = b, a % b
    return a


def is_power(n: int) -> Optional[Tuple[int, int]]:
    """
    Check if n is a perfect power, i.e., n = a^b for some a, b > 1.
    
    Args:
        n: The number to check
        
    Returns:
        Tuple (a, b) if n = a^b, None otherwise
    """
    for b in range(2, int(math.log2(n)) + 1):
        a = round(n ** (1/b))
        if a ** b == n:
            return (a, b)
    return None


def continued_fraction_expansion(numerator: int, denominator: int, max_terms: int = 20) -> List[int]:
    """
    Compute the continued fraction expansion of numerator/denominator.
    
    Args:
        numerator: Numerator of the fraction
        denominator: Denominator of the fraction
        max_terms: Maximum number of terms to compute
        
    Returns:
        List of continued fraction coefficients
    """
    cf = []
    for _ in range(max_terms):
        if denominator == 0:
            break
        q = numerator // denominator
        cf.append(q)
        numerator, denominator = denominator, numerator - q * denominator
    return cf


def convergents_from_cf(cf: List[int]) -> List[Tuple[int, int]]:
    """
    Compute the convergents from a continued fraction expansion.
    
    Args:
        cf: Continued fraction coefficients
        
    Returns:
        List of convergents as (numerator, denominator) tuples
    """
    convergents = []
    for i in range(len(cf)):
        if i == 0:
            convergents.append((cf[0], 1))
        elif i == 1:
            convergents.append((cf[1] * cf[0] + 1, cf[1]))
        else:
            num = cf[i] * convergents[i-1][0] + convergents[i-2][0]
            den = cf[i] * convergents[i-1][1] + convergents[i-2][1]
            convergents.append((num, den))
    return convergents


def quantum_period_finding(a: int, N: int, n_count: int = 8, use_simulator: bool = True) -> Optional[int]:
    """
    Find the period of a^x mod N using quantum period finding.
    This is the quantum subroutine of Shor's algorithm.
    
    Args:
        a: Base for modular exponentiation
        N: The modulus
        n_count: Number of counting qubits (affects precision)
        use_simulator: Whether to use simulator or real quantum hardware
        
    Returns:
        The period r, or None if not found
    """
    # Number of qubits needed to represent N
    n_target = math.ceil(math.log2(N))
    
    # Create quantum circuit
    qr_count = QuantumRegister(n_count, 'counting')
    qr_target = QuantumRegister(n_target, 'target')
    cr = ClassicalRegister(n_count, 'measure')
    qc = QuantumCircuit(qr_count, qr_target, cr)
    
    # Initialize counting qubits in superposition
    for q in range(n_count):
        qc.h(qr_count[q])
    
    # Initialize target register to |1⟩
    qc.x(qr_target[0])
    
    # Controlled modular exponentiation
    for q in range(n_count):
        # Apply a^(2^q) mod N controlled by counting qubit q
        power = 2 ** q
        value = pow(a, power, N)
        qc.append(controlled_modular_mult(value, N, n_target).control(1), 
                  [qr_count[q]] + list(qr_target))
    
    # Apply inverse QFT on counting qubits
    qft_inv = QFT(n_count, inverse=True)
    qc.append(qft_inv, qr_count)
    
    # Measure counting qubits
    qc.measure(qr_count, cr)
    
    # Execute circuit
    if use_simulator:
        from qiskit_aer import Aer
        backend = Aer.get_backend('qasm_simulator')
        from qiskit import transpile
        transpiled_qc = transpile(qc, backend)
        job = backend.run(transpiled_qc, shots=1000)
        result = job.result()
        counts = result.get_counts()
    else:
        # Run on IBM Quantum hardware
        # Note: This requires proper IBM Quantum credentials
        try:
            service = QiskitRuntimeService()
            backend = service.least_busy(operational=True, simulator=False)
            with Session(service=service, backend=backend) as session:
                sampler = Sampler(session=session)
                job = sampler.run(qc, shots=1000)
                result = job.result()
                counts = result.quasi_dists[0]
        except Exception as e:
            print(f"Error running on quantum hardware: {e}")
            print("Falling back to simulator...")
            return quantum_period_finding(a, N, n_count, use_simulator=True)
    
    # Process measurement results
    # Find the most common measurement outcome
    measured_phases = []
    for output in counts:
        decimal = int(output, 2)
        phase = decimal / (2 ** n_count)
        measured_phases.append(phase)
    
    # Use most frequent phase
    if not measured_phases:
        return None
    
    phase = max(set(measured_phases), key=measured_phases.count)
    
    # Use continued fractions to find period
    if phase == 0:
        return None
    
    frac = Fraction(phase).limit_denominator(N)
    r = frac.denominator
    
    # Verify the period
    if pow(a, r, N) == 1:
        return r
    
    # Try other convergents
    cf = continued_fraction_expansion(int(phase * (2**n_count)), 2**n_count)
    convergents = convergents_from_cf(cf)
    
    for num, den in convergents:
        if den > 0 and den < N:
            if pow(a, den, N) == 1:
                return den
    
    return None


def controlled_modular_mult(a: int, N: int, n: int) -> QuantumCircuit:
    """
    Create a circuit for controlled modular multiplication by a mod N.
    
    This is a simplified placeholder implementation.
    A full implementation would require proper modular arithmetic circuits.
    
    Args:
        a: Multiplier
        N: Modulus
        n: Number of qubits
        
    Returns:
        Quantum circuit for controlled modular multiplication
    """
    qr = QuantumRegister(n)
    qc = QuantumCircuit(qr)
    
    # Simplified implementation - in practice, this would be more complex
    # This is a placeholder that represents the modular exponentiation
    for i in range(n):
        if a & (1 << i):
            qc.x(qr[i])
    
    return qc


def shors_algorithm(N: int, use_simulator: bool = True, max_attempts: int = 10) -> Optional[List[int]]:
    """
    Factor an integer N using Shor's algorithm.
    
    Args:
        N: The integer to factor
        use_simulator: Whether to use quantum simulator or real hardware
        max_attempts: Maximum number of attempts to find factors
        
    Returns:
        List of non-trivial factors, or None if factorization fails
    """
    # Handle edge cases
    if N < 2:
        return None
    
    if N % 2 == 0:
        return [2, N // 2]
    
    # Check if N is a prime power
    power_result = is_power(N)
    if power_result:
        base, exp = power_result
        return [base] * exp
    
    # Main loop - try different random values of a
    for attempt in range(max_attempts):
        # Pick a random a < N
        a = random.randint(2, N - 1)
        
        # Check if a and N are coprime
        g = gcd(a, N)
        if g > 1:
            # Lucky case - we found a factor directly
            return [g, N // g]
        
        # Find the period using quantum period finding
        print(f"Attempt {attempt + 1}: Finding period of {a}^x mod {N}...")
        r = quantum_period_finding(a, N, n_count=8, use_simulator=use_simulator)
        
        if r is None or r % 2 != 0:
            print(f"  Period finding unsuccessful or period is odd, trying again...")
            continue
        
        # Check if we found a non-trivial factor
        x = pow(a, r // 2, N)
        
        if x == N - 1:
            print(f"  Period {r} gives x ≡ -1 (mod N), trying again...")
            continue
        
        factor1 = gcd(x + 1, N)
        factor2 = gcd(x - 1, N)
        
        if factor1 > 1 and factor1 < N:
            print(f"  Success! Found factors: {factor1} and {N // factor1}")
            return [factor1, N // factor1]
        
        if factor2 > 1 and factor2 < N:
            print(f"  Success! Found factors: {factor2} and {N // factor2}")
            return [factor2, N // factor2]
    
    print(f"Failed to factor {N} after {max_attempts} attempts")
    return None


def shors_algorithm_simple(N: int) -> Optional[List[int]]:
    """
    Simplified version of Shor's algorithm for demonstration.
    Uses classical period finding as a fallback for educational purposes.
    
    Args:
        N: The integer to factor
        
    Returns:
        List of factors
    """
    # Handle edge cases
    if N < 2:
        return None
    
    if N % 2 == 0:
        return [2, N // 2]
    
    # Check if N is a prime power
    power_result = is_power(N)
    if power_result:
        base, exp = power_result
        return [base] * exp
    
    # Try classical period finding for small numbers
    for _ in range(10):
        a = random.randint(2, N - 1)
        g = gcd(a, N)
        
        if g > 1:
            return [g, N // g]
        
        # Classical period finding (for demonstration)
        r = classical_period_finding(a, N)
        
        if r and r % 2 == 0:
            x = pow(a, r // 2, N)
            if x != N - 1:
                factor1 = gcd(x + 1, N)
                factor2 = gcd(x - 1, N)
                
                if factor1 > 1 and factor1 < N:
                    return [factor1, N // factor1]
                if factor2 > 1 and factor2 < N:
                    return [factor2, N // factor2]
    
    return None


def classical_period_finding(a: int, N: int, max_period: int = 1000) -> Optional[int]:
    """
    Find the period of a^x mod N classically (for small numbers).
    
    Args:
        a: Base
        N: Modulus
        max_period: Maximum period to search
        
    Returns:
        The period r such that a^r ≡ 1 (mod N)
    """
    if gcd(a, N) != 1:
        return None
    
    power = a % N
    for r in range(1, min(max_period, N)):
        if power == 1:
            return r
        power = (power * a) % N
    
    return None
