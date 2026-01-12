#!/usr/bin/env python3
"""
Simple example demonstrating the factorization comparison framework.
This script shows basic usage without requiring command-line arguments.
"""

from classical_factorization import trial_division, pollard_rho_factorize
from comparison import compare_algorithms, print_comparison_summary

# Example numbers to factorize
example_numbers = [
    15,   # 3 × 5 (small composite)
    77,   # 7 × 11 (semiprime)
    143,  # 11 × 13 (semiprime)
]

print("="*80)
print("SIMPLE FACTORIZATION EXAMPLE")
print("="*80)
print()

# Individual algorithm examples
print("Example 1: Using individual algorithms")
print("-" * 80)

number = 77
print(f"\nFactorizing {number} using different methods:")

factors_td = trial_division(number)
print(f"  Trial Division:  {number} = {' × '.join(map(str, factors_td))}")

factors_pr = pollard_rho_factorize(number)
print(f"  Pollard's Rho:   {number} = {' × '.join(map(str, factors_pr))}")

print()
print("="*80)
print()

# Comparison example
print("Example 2: Comparing algorithms with benchmarking")
print("-" * 80)
print(f"\nComparing algorithms on numbers: {example_numbers}")
print()

results = compare_algorithms(example_numbers, use_quantum=False)
print_comparison_summary(results)

print()
print("="*80)
print("For more options, run: python main.py --help")
print("="*80)
