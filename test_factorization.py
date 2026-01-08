"""
Basic tests for the factorization algorithms.
Run with: python test_factorization.py
"""

import sys
from classical_factorization import trial_division, pollard_rho_factorize, fermat_factorization
from shors_algorithm import gcd, is_power, classical_period_finding


def test_trial_division():
    """Test trial division algorithm."""
    print("Testing trial_division...")
    
    test_cases = [
        (15, [3, 5]),
        (77, [7, 11]),
        (143, [11, 13]),
        (100, [2, 2, 5, 5]),
    ]
    
    for number, expected in test_cases:
        result = trial_division(number)
        assert result == expected, f"Failed for {number}: expected {expected}, got {result}"
        print(f"  ✓ {number} = {' × '.join(map(str, result))}")
    
    print("  All trial_division tests passed!\n")


def test_pollard_rho():
    """Test Pollard's rho algorithm."""
    print("Testing pollard_rho_factorize...")
    
    test_cases = [
        (15, [3, 5]),
        (77, [7, 11]),
        (143, [11, 13]),
    ]
    
    for number, expected in test_cases:
        result = pollard_rho_factorize(number)
        # Check that product equals original
        product = 1
        for f in result:
            product *= f
        assert product == number, f"Failed for {number}: factors don't multiply correctly"
        print(f"  ✓ {number} = {' × '.join(map(str, result))}")
    
    print("  All pollard_rho_factorize tests passed!\n")


def test_fermat():
    """Test Fermat's factorization."""
    print("Testing fermat_factorization...")
    
    test_cases = [
        (15, (3, 5)),
        (77, (7, 11)),
        (143, (11, 13)),
    ]
    
    for number, expected_factors in test_cases:
        result = fermat_factorization(number)
        assert result is not None, f"Failed for {number}: returned None"
        # Check that product equals original
        product = result[0] * result[1]
        assert product == number, f"Failed for {number}: factors don't multiply correctly"
        print(f"  ✓ {number} = {result[0]} × {result[1]}")
    
    print("  All fermat_factorization tests passed!\n")


def test_gcd():
    """Test greatest common divisor."""
    print("Testing gcd...")
    
    test_cases = [
        (48, 18, 6),
        (100, 50, 50),
        (17, 19, 1),
        (21, 14, 7),
    ]
    
    for a, b, expected in test_cases:
        result = gcd(a, b)
        assert result == expected, f"Failed for gcd({a}, {b}): expected {expected}, got {result}"
        print(f"  ✓ gcd({a}, {b}) = {result}")
    
    print("  All gcd tests passed!\n")


def test_is_power():
    """Test power detection."""
    print("Testing is_power...")
    
    # Perfect powers
    result = is_power(8)
    assert result == (2, 3), f"8 = 2^3, got {result}"
    print("  ✓ 8 = 2^3")
    
    result = is_power(27)
    assert result == (3, 3), f"27 = 3^3, got {result}"
    print("  ✓ 27 = 3^3")
    
    result = is_power(16)
    # 16 can be 2^4 or 4^2, either is correct
    assert result is not None, "16 should be detected as a perfect power"
    a, b = result
    assert a ** b == 16, f"16 = {a}^{b} should equal 16"
    print(f"  ✓ 16 = {a}^{b}")
    
    # Non-powers
    assert is_power(15) is None, "15 is not a perfect power"
    assert is_power(77) is None, "77 is not a perfect power"
    print("  ✓ 15 is not a perfect power")
    print("  ✓ 77 is not a perfect power")
    
    print("  All is_power tests passed!\n")


def test_classical_period_finding():
    """Test classical period finding."""
    print("Testing classical_period_finding...")
    
    # Test some known periods
    # For a=2, N=15: 2^1=2, 2^2=4, 2^3=8, 2^4=16≡1 (mod 15), so period=4
    result = classical_period_finding(2, 15)
    assert result == 4, f"Failed for a=2, N=15: expected 4, got {result}"
    print(f"  ✓ Period of 2 mod 15 = {result}")
    
    # For a=3, N=10: 3^1=3, 3^2=9, 3^3=27≡7, 3^4=81≡1 (mod 10), so period=4
    result = classical_period_finding(3, 10)
    assert result == 4, f"Failed for a=3, N=10: expected 4, got {result}"
    print(f"  ✓ Period of 3 mod 10 = {result}")
    
    print("  All classical_period_finding tests passed!\n")


def run_all_tests():
    """Run all tests."""
    print("="*80)
    print("RUNNING FACTORIZATION TESTS")
    print("="*80)
    print()
    
    try:
        test_trial_division()
        test_pollard_rho()
        test_fermat()
        test_gcd()
        test_is_power()
        test_classical_period_finding()
        
        print("="*80)
        print("ALL TESTS PASSED! ✓")
        print("="*80)
        return 0
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("="*80)
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("="*80)
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
