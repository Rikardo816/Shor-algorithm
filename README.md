# Shor's Algorithm: Classical vs. Quantum Factorization

This project is part of my thesis, in which I compare classical algorithms for number factorization with Shor's algorithm running on IBM quantum computers.

## Overview

This repository contains implementations of:
- **Classical factorization algorithms**: Trial division, Pollard's rho, and Fermat's factorization
- **Shor's quantum algorithm**: Implementation using Qiskit for IBM quantum computers
- **Comparison framework**: Tools to benchmark and compare the performance of different algorithms

## Features

- 🔢 Multiple classical factorization algorithms
- ⚛️ Shor's quantum algorithm implementation using Qiskit
- 📊 Performance benchmarking and comparison tools
- 📝 Detailed reporting in JSON format
- 🖥️ Support for both quantum simulators and real IBM quantum hardware

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Rikardo816/Shor-algorithm.git
cd Shor-algorithm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the example:
```bash
python example.py
```

### Optional: IBM Quantum Setup

To use Shor's algorithm on real IBM quantum hardware:
   - Create an account at [IBM Quantum](https://quantum.ibm.com/)
   - Get your API token from the dashboard
   - Save your credentials:
   ```python
   from qiskit_ibm_runtime import QiskitRuntimeService
   QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_TOKEN")
   ```

## Usage

### Basic Usage

Run with default demo numbers:
```bash
python main.py
```

### Custom Numbers

Factorize specific numbers:
```bash
python main.py --numbers 15 21 77 143 221
```

### Test Suite

Run comprehensive test suite:
```bash
python main.py --test-suite
```

### Quantum Mode

Include Shor's algorithm (requires IBM Quantum credentials):
```bash
python main.py --use-quantum --numbers 15 21 35
```

### Custom Output

Specify output file for results:
```bash
python main.py --output my_results.json --numbers 77 143 221
```

## Algorithms Implemented

### Classical Algorithms

1. **Trial Division**: 
   - Simple but effective for numbers with small prime factors
   - Time complexity: O(√n)

2. **Pollard's Rho**:
   - Probabilistic algorithm for finding factors
   - Effective for numbers with factors of similar size
   - Time complexity: O(n^(1/4))

3. **Fermat's Factorization**:
   - Works well for products of two primes close in magnitude
   - Based on difference of squares

### Quantum Algorithm

**Shor's Algorithm**:
- Quantum algorithm for integer factorization
- Uses quantum period finding as a subroutine
- Exponentially faster than classical algorithms (in theory)
- Time complexity: O((log n)³)
- Requires quantum computer or simulator

## Project Structure

```
Shor-algorithm/
├── main.py                      # Main execution script
├── example.py                   # Simple example/demo script
├── classical_factorization.py   # Classical algorithms implementation
├── shors_algorithm.py          # Shor's algorithm implementation
├── comparison.py               # Benchmarking and comparison tools
├── requirements.txt            # Python dependencies
├── .env.example               # Example configuration file
└── README.md                  # This file
```

## Example Output

```
================================================================================
FACTORIZATION ALGORITHM COMPARISON
Thesis Project: Classical vs. Quantum Factorization (Shor's Algorithm)
================================================================================

============================================================
Factorizing: 77
============================================================

Running Trial Division...
Trial Division:
  Number: 77
  Factors: 7 × 11
  Time: 0.000015 seconds
  Verified: True

Running Pollard's Rho...
Pollard's Rho:
  Number: 77
  Factors: 7 × 11
  Time: 0.000234 seconds
  Verified: True

================================================================================
COMPARISON SUMMARY
================================================================================

Number: 77
--------------------------------------------------------------------------------
Algorithm                 Success    Time (s)        Speedup   
--------------------------------------------------------------------------------
trial_division            ✓          0.000015        1.00x     
pollard_rho              ✓          0.000234        0.06x     
fermat                   ✓          0.000089        0.17x     
================================================================================

Comparison report saved to: comparison_report.json
```

## Output Format

Results are saved in JSON format with the following structure:
```json
{
  "summary": [
    {
      "number": 77,
      "algorithms": {
        "trial_division": {
          "success": true,
          "time_seconds": 0.000015
        }
      }
    }
  ],
  "detailed_results": [...]
}
```

## Thesis Context

This project demonstrates the theoretical advantages of quantum computing for factorization problems:

- **Classical complexity**: Best known classical algorithms run in sub-exponential time
- **Quantum advantage**: Shor's algorithm runs in polynomial time on a quantum computer
- **Practical considerations**: Current quantum computers have limitations (noise, limited qubits)

The comparison helps illustrate:
1. The performance of different classical approaches
2. The potential of quantum algorithms
3. The current state of quantum hardware capabilities

## IBM Quantum Hardware

When using `--use-quantum` flag, the implementation can:
- Use Qiskit Aer simulator for testing
- Connect to IBM Quantum cloud services
- Run on real quantum hardware (subject to availability and queue times)

Note: Real quantum hardware execution requires:
- IBM Quantum account
- Valid API token
- Access to quantum systems (free tier available)

## Limitations

- Quantum implementation requires significant qubits for large numbers
- Current quantum hardware has noise and error rates
- Simulator mode is used by default for reliability
- Classical algorithms may be faster for small numbers

## Contributing

This is a thesis project, but suggestions and improvements are welcome!

## License

This project is part of academic research. Please cite appropriately if used in academic work.

## References

- Shor, P. W. (1997). "Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer"
- Qiskit Documentation: https://qiskit.org/
- IBM Quantum: https://quantum.ibm.com/

## Author

Ricardo - Thesis Project on Quantum Computing and Factorization Algorithms

## Acknowledgments

- IBM Quantum for providing access to quantum computers
- Qiskit development team
- Academic advisors and reviewers
