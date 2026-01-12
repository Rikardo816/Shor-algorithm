"""
Classical Factorization Algorithms
This module implements various classical algorithms for integer factorization.
"""

import math
import random
from typing import List, Tuple, Optional


# Constants for primality testing
SMALL_PRIME_LIMIT = 1000  # Limit for simple primality test iteration
PRIME_THRESHOLD = 1000000  # Threshold for assuming a number might be prime


def trial_division(n: int) -> List[int]:
    """
    Factor a number using trial division.
    
    Args:
        n: The number to factor
        
    Returns:
        List of prime factors
    """
    if n < 2:
        return []
    
    factors = []
    
    # Check for factor 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # Check odd factors up to sqrt(n)
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    
    # If n is a prime greater than 2
    if n > 2:
        factors.append(n)
    
    return factors


def gcd(a: int, b: int) -> int:
    """
    Compute the greatest common divisor using Euclidean algorithm.
    
    Args:
        a: First integer
        b: Second integer
        
    Returns:
        Greatest common divisor of a and b
    """
    while b:
        a, b = b, a % b
    return a


def pollard_rho(n: int, max_iterations: int = 100000) -> Optional[int]:
    """
    Factor a number using Pollard's rho algorithm.
    
    Args:
        n: The number to factor
        max_iterations: Maximum number of iterations
        
    Returns:
        A non-trivial factor of n, or None if not found
    """
    if n % 2 == 0:
        return 2
    
    # Random function parameters
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    
    iteration = 0
    while d == 1 and iteration < max_iterations:
        # Tortoise move
        x = (x * x + c) % n
        # Hare move (twice as fast)
        y = (y * y + c) % n
        y = (y * y + c) % n
        # Check for cycle
        d = gcd(abs(x - y), n)
        iteration += 1
    
    if d != n:
        return d
    return None


def pollard_rho_factorize(n: int) -> List[int]:
    """
    Completely factor a number using Pollard's rho algorithm.
    
    Args:
        n: The number to factor
        
    Returns:
        List of prime factors
    """
    if n < 2:
        return []
    
    if n == 2:
        return [2]
    
    # Check if n is prime (simple primality test)
    if all(n % i != 0 for i in range(2, min(int(n**0.5) + 1, SMALL_PRIME_LIMIT))):
        if n < PRIME_THRESHOLD:
            return [n]
    
    factors = []
    
    # Try to find a factor
    factor = pollard_rho(n)
    
    if factor is None or factor == n:
        # Fall back to trial division for small numbers
        if n < 10000:
            return trial_division(n)
        return [n]  # Assume prime if we can't factor
    
    # Recursively factor
    factors.extend(pollard_rho_factorize(factor))
    factors.extend(pollard_rho_factorize(n // factor))
    
    return sorted(factors)


def fermat_factorization(n: int, max_iterations: int = 100000) -> Optional[Tuple[int, int]]:
    """
    Factor a number using Fermat's factorization method.
    Works well for numbers that are products of two primes of similar magnitude.
    
    Args:
        n: The number to factor
        max_iterations: Maximum number of iterations
        
    Returns:
        A tuple (a, b) such that n = a * b, or None if not found
    """
    if n % 2 == 0:
        return (2, n // 2)
    
    a = math.ceil(math.sqrt(n))
    b_sq = a * a - n
    
    iteration = 0
    while iteration < max_iterations:
        b = int(math.sqrt(b_sq))
        if b * b == b_sq:
            return (a - b, a + b)
        a += 1
        b_sq = a * a - n
        iteration += 1
    
    return None


def is_prime_simple(n: int) -> bool:
    """
    Simple primality test for small numbers.
    
    Args:
        n: The number to test
        
    Returns:
        True if n is likely prime, False otherwise
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, min(int(n**0.5) + 1, SMALL_PRIME_LIMIT), 2):
        if n % i == 0:
            return False
    
    return True
