#!/usr/bin/env python3
"""
Main execution script for comparing classical and quantum factorization algorithms.
This is the entry point for the thesis project comparing Shor's algorithm with classical methods.
"""

import argparse
import sys

from comparison import (
    compare_algorithms,
    generate_comparison_report,
    print_comparison_summary,
    generate_test_numbers
)


def main():
    """Main function to run algorithm comparisons."""
    parser = argparse.ArgumentParser(
        description="Compare classical and quantum factorization algorithms"
    )
    
    parser.add_argument(
        '--numbers',
        type=int,
        nargs='+',
        help='List of numbers to factorize (e.g., --numbers 15 21 35)'
    )
    
    parser.add_argument(
        '--use-quantum',
        action='store_true',
        help='Include Shor\'s quantum algorithm (requires IBM Quantum credentials)'
    )
    
    parser.add_argument(
        '--test-suite',
        action='store_true',
        help='Run a predefined test suite of numbers'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='comparison_report.json',
        help='Output file for comparison report (default: comparison_report.json)'
    )
    
    args = parser.parse_args()
    
    # Determine which numbers to factorize
    if args.test_suite:
        numbers = generate_test_numbers()
        print("Running test suite with predefined numbers...")
    elif args.numbers:
        numbers = args.numbers
    else:
        # Default demo numbers
        numbers = [15, 21, 77, 143, 221]
        print("No numbers specified. Using default demo set: [15, 21, 77, 143, 221]")
        print("Use --numbers to specify custom numbers or --test-suite for full test suite.")
    
    print("\n" + "="*80)
    print("FACTORIZATION ALGORITHM COMPARISON")
    print("Thesis Project: Classical vs. Quantum Factorization (Shor's Algorithm)")
    print("="*80)
    
    if args.use_quantum:
        print("\nQuantum mode enabled: Will attempt to use Shor's algorithm")
        print("Note: This requires IBM Quantum credentials configured.")
    else:
        print("\nClassical mode only: Using trial division, Pollard's rho, and Fermat's method")
        print("Use --use-quantum to enable Shor's algorithm")
    
    # Run comparisons
    results = compare_algorithms(numbers, use_quantum=args.use_quantum)
    
    # Print summary
    print_comparison_summary(results)
    
    # Generate detailed report
    generate_comparison_report(results, args.output)
    
    print("\n" + "="*80)
    print("Comparison complete!")
    print(f"Detailed results saved to: {args.output}")
    print("="*80)


if __name__ == "__main__":
    main()
