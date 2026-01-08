"""
Comparison and Benchmarking Module
This module provides utilities to compare classical and quantum factorization algorithms.
"""

import time
from typing import Dict, List, Tuple, Callable, Optional
import json

from classical_factorization import (
    trial_division,
    pollard_rho_factorize,
    fermat_factorization
)
from shors_algorithm import shors_algorithm_simple


class FactorizationResult:
    """Class to store factorization results."""
    
    def __init__(self, number: int, algorithm: str, factors: Optional[List[int]], 
                 time_taken: float, success: bool):
        self.number = number
        self.algorithm = algorithm
        self.factors = factors if factors else []
        self.time_taken = time_taken
        self.success = success
    
    def to_dict(self) -> Dict:
        """Convert result to dictionary."""
        return {
            'number': self.number,
            'algorithm': self.algorithm,
            'factors': self.factors,
            'time_seconds': self.time_taken,
            'success': self.success,
            'product_check': self.verify_factors()
        }
    
    def verify_factors(self) -> bool:
        """Verify that the factors multiply to give the original number."""
        if not self.factors:
            return False
        product = 1
        for f in self.factors:
            product *= f
        return product == self.number
    
    def __str__(self) -> str:
        """String representation of the result."""
        if self.success:
            factors_str = ' × '.join(map(str, self.factors))
            return (f"{self.algorithm}:\n"
                   f"  Number: {self.number}\n"
                   f"  Factors: {factors_str}\n"
                   f"  Time: {self.time_taken:.6f} seconds\n"
                   f"  Verified: {self.verify_factors()}")
        else:
            return (f"{self.algorithm}:\n"
                   f"  Number: {self.number}\n"
                   f"  Status: Failed\n"
                   f"  Time: {self.time_taken:.6f} seconds")


def benchmark_algorithm(algorithm_func: Callable, number: int, 
                       algorithm_name: str) -> FactorizationResult:
    """
    Benchmark a factorization algorithm.
    
    Args:
        algorithm_func: Function that performs factorization
        number: Number to factorize
        algorithm_name: Name of the algorithm for reporting
        
    Returns:
        FactorizationResult object with timing and result information
    """
    start_time = time.time()
    
    try:
        factors = algorithm_func(number)
        elapsed_time = time.time() - start_time
        
        if factors and len(factors) > 0:
            return FactorizationResult(number, algorithm_name, factors, 
                                      elapsed_time, True)
        else:
            return FactorizationResult(number, algorithm_name, None, 
                                      elapsed_time, False)
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"Error in {algorithm_name}: {e}")
        return FactorizationResult(number, algorithm_name, None, 
                                   elapsed_time, False)


def compare_algorithms(numbers: List[int], 
                      use_quantum: bool = False) -> List[Dict[str, FactorizationResult]]:
    """
    Compare different factorization algorithms on a list of numbers.
    
    Args:
        numbers: List of numbers to factorize
        use_quantum: Whether to include quantum algorithm (requires IBM Quantum access)
        
    Returns:
        List of dictionaries containing results for each number
    """
    results = []
    
    for number in numbers:
        print(f"\n{'='*60}")
        print(f"Factorizing: {number}")
        print(f"{'='*60}")
        
        number_results = {}
        
        # Trial Division
        print("\nRunning Trial Division...")
        number_results['trial_division'] = benchmark_algorithm(
            trial_division, number, "Trial Division"
        )
        print(number_results['trial_division'])
        
        # Pollard's Rho
        print("\nRunning Pollard's Rho...")
        number_results['pollard_rho'] = benchmark_algorithm(
            pollard_rho_factorize, number, "Pollard's Rho"
        )
        print(number_results['pollard_rho'])
        
        # Fermat's Factorization
        print("\nRunning Fermat's Factorization...")
        number_results['fermat'] = benchmark_algorithm(
            fermat_factorization_wrapper, number, "Fermat's Factorization"
        )
        print(number_results['fermat'])
        
        # Shor's Algorithm (if enabled)
        if use_quantum:
            print("\nRunning Shor's Algorithm...")
            number_results['shors'] = benchmark_algorithm(
                shors_algorithm_simple, number, "Shor's Algorithm"
            )
            print(number_results['shors'])
        
        results.append({
            'number': number,
            'results': number_results
        })
    
    return results


def generate_comparison_report(results: List[Dict[str, FactorizationResult]], 
                               output_file: str = "comparison_report.json") -> None:
    """
    Generate a detailed comparison report.
    
    Args:
        results: List of comparison results
        output_file: Output file path for JSON report
    """
    report = {
        'summary': [],
        'detailed_results': []
    }
    
    for item in results:
        number = item['number']
        number_results = item['results']
        
        # Summary for this number
        summary = {
            'number': number,
            'algorithms': {}
        }
        
        detailed = {
            'number': number,
            'results': {}
        }
        
        for algo_name, result in number_results.items():
            summary['algorithms'][algo_name] = {
                'success': result.success,
                'time_seconds': result.time_taken
            }
            detailed['results'][algo_name] = result.to_dict()
        
        report['summary'].append(summary)
        report['detailed_results'].append(detailed)
    
    # Write report to file
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n\nComparison report saved to: {output_file}")


def print_comparison_summary(results: List[Dict[str, FactorizationResult]]) -> None:
    """
    Print a summary table of comparison results.
    
    Args:
        results: List of comparison results
    """
    print("\n" + "="*80)
    print("COMPARISON SUMMARY")
    print("="*80)
    
    for item in results:
        number = item['number']
        number_results = item['results']
        
        print(f"\nNumber: {number}")
        print("-" * 80)
        print(f"{'Algorithm':<25} {'Success':<10} {'Time (s)':<15} {'Speedup':<10}")
        print("-" * 80)
        
        # Find baseline time (trial division)
        baseline_time = number_results.get('trial_division')
        baseline = baseline_time.time_taken if baseline_time and baseline_time.success else None
        
        for algo_name, result in number_results.items():
            success_str = "✓" if result.success else "✗"
            time_str = f"{result.time_taken:.6f}"
            
            if baseline and result.success and result.time_taken > 0:
                speedup = baseline / result.time_taken
                speedup_str = f"{speedup:.2f}x"
            else:
                speedup_str = "N/A"
            
            print(f"{algo_name:<25} {success_str:<10} {time_str:<15} {speedup_str:<10}")
    
    print("="*80)


def generate_test_numbers() -> List[int]:
    """
    Generate a list of test numbers for factorization comparison.
    
    Returns:
        List of test numbers with varying characteristics
    """
    test_numbers = [
        # Small composite numbers
        15,      # 3 × 5
        21,      # 3 × 7
        35,      # 5 × 7
        
        # Products of two primes
        77,      # 7 × 11
        143,     # 11 × 13
        221,     # 13 × 17
        
        # Larger semiprimes
        1147,    # 31 × 37
        2021,    # 43 × 47
        4087,    # 61 × 67
        
        # Numbers with small factors
        256,     # 2^8
        1000,    # 2^3 × 5^3
        
        # Harder to factor (close primes)
        899,     # 29 × 31
        4757,    # 67 × 71
    ]
    
    return test_numbers


def fermat_factorization_wrapper(n: int) -> Optional[List[int]]:
    """
    Wrapper function for Fermat's factorization that returns a list format.
    
    Args:
        n: Number to factorize
        
    Returns:
        List of factors or None if factorization fails
    """
    result = fermat_factorization(n)
    if result:
        return list(result)
    return None
