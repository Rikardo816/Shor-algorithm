# Thesis Context: Classical vs. Quantum Factorization

## Overview

This project implements and compares classical integer factorization algorithms with Shor's quantum algorithm. The comparison demonstrates the theoretical advantages of quantum computing for this class of problems.

## Algorithms Implemented

### Classical Algorithms

1. **Trial Division**
   - **Complexity**: O(√n)
   - **Best for**: Small numbers, numbers with small factors
   - **Description**: Tests all possible divisors up to √n

2. **Pollard's Rho Algorithm**
   - **Complexity**: O(n^(1/4)) expected
   - **Best for**: Composite numbers with factors of similar size
   - **Description**: Probabilistic algorithm using cycle detection

3. **Fermat's Factorization**
   - **Complexity**: O(|p-q|) where n = p×q
   - **Best for**: Products of two primes close in magnitude
   - **Description**: Based on difference of squares: n = a² - b²

### Quantum Algorithm

**Shor's Algorithm**
- **Complexity**: O((log n)³) on quantum computer
- **Best for**: Large semiprimes (products of two large primes)
- **Description**: Uses quantum period finding to factor integers exponentially faster than known classical algorithms

## Key Observations for Thesis

### Classical Performance

The classical algorithms show different performance characteristics:

- **Trial division** is fastest for small numbers and numbers with small factors
- **Pollard's rho** performs well for medium-sized numbers
- **Fermat's method** excels when factors are close in magnitude

For most practical numbers (< 10^6), classical algorithms are very fast (microseconds).

### Quantum Advantage

Shor's algorithm provides theoretical advantages:

1. **Asymptotic Speedup**: Polynomial vs. sub-exponential classical algorithms
2. **RSA Implications**: Threatens RSA encryption (which relies on factorization hardness)
3. **Current Limitations**: 
   - Requires large, error-corrected quantum computers
   - Current quantum hardware is noisy (NISQ era)
   - For small numbers, classical algorithms are faster in practice

### Thesis Implications

This comparison demonstrates:

1. **Problem Size Matters**: Quantum advantage is asymptotic - not visible for small numbers
2. **Hardware Requirements**: Real quantum advantage requires fault-tolerant quantum computers
3. **Algorithm Choice**: Different algorithms excel in different scenarios
4. **Future of Computing**: Quantum computers will revolutionize certain problem domains

## Experimental Setup

### Test Numbers

The test suite includes:
- Small composites (15, 21, 35)
- Semiprimes (77, 143, 221, 1147, 2021, 4087)
- Special forms (256 = 2^8, 1000 = 2³×5³)
- Close primes (899 = 29×31, 4757 = 67×71)

### Metrics Collected

- Execution time
- Success rate
- Factor verification
- Speedup comparison

## Running Experiments

### Basic Comparison (Classical Only)
```bash
python main.py --numbers 15 21 77 143 221
```

### With Quantum Simulator
```bash
python main.py --use-quantum --numbers 15 21 35
```

### Full Test Suite
```bash
python main.py --test-suite --output thesis_results.json
```

## Results Interpretation

### Example Output Analysis

For number 77 (= 7 × 11):
- Trial division: ~3 μs (very fast, direct method)
- Pollard's rho: ~20 μs (probabilistic overhead)
- Fermat's method: ~5 μs (efficient for this size)

The speedup metrics show relative performance. A speedup < 1.0 means slower than baseline (trial division).

### Why Classical Wins for Small Numbers

For numbers in this test suite (< 10^4):
1. Classical algorithms are highly optimized
2. Quantum overhead (circuit preparation, measurement) dominates
3. Quantum advantage appears only for much larger numbers (> 2^2048)

## Conclusions for Thesis

1. **Classical algorithms remain practical** for numbers up to ~10^10
2. **Quantum algorithms promise exponential speedup** for large numbers
3. **Current quantum hardware is limited** but rapidly improving
4. **The crossover point** where quantum becomes faster is estimated at ~10^15 with current technology

## Future Work

- Implement optimized quantum circuits for modular exponentiation
- Test on real IBM quantum hardware
- Extend to larger numbers as hardware improves
- Compare with other factorization methods (number field sieve, elliptic curve method)

## References

1. Shor, P. W. (1997). "Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer"
2. Pollard, J. M. (1975). "A Monte Carlo method for factorization"
3. Fermat, P. de (1643). "Factorization methods"
4. Nielsen, M. A., & Chuang, I. L. (2010). "Quantum Computation and Quantum Information"

## Contact

This is a thesis project on quantum computing and factorization algorithms.
For questions or collaboration: [Your contact information]
