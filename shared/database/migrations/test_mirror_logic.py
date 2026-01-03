#!/usr/bin/env python3
"""
Test the mirror logic for F2L setup sequences.
Verifies that the mirroring transformation is correct.
"""

from fix_f2l_setup_sequences import mirror_move, mirror_moves

def test_single_moves():
    """Test individual move mirroring"""
    print("=== Single Move Mirror Tests ===\n")

    test_cases = [
        # R ↔ L with prime swap
        ("R", "L'"),
        ("R'", "L"),
        ("R2", "L2"),
        ("R2'", "L2'"),
        ("L", "R'"),
        ("L'", "R"),
        ("L2", "R2"),

        # F, U, B, D - flip prime only
        ("F", "F'"),
        ("F'", "F"),
        ("F2", "F2"),
        ("U", "U'"),
        ("U'", "U"),
        ("U2", "U2"),
        ("B", "B'"),
        ("B'", "B"),
        ("D", "D'"),
        ("D'", "D"),

        # Wide moves
        ("r", "l'"),
        ("r'", "l"),
        ("l", "r'"),
        ("l'", "r"),

        # Slice moves - M and E are symmetric, S follows F
        ("M", "M"),
        ("M'", "M'"),
        ("M2", "M2"),
        ("S", "S'"),
        ("S'", "S"),

        # Rotations
        ("y", "y'"),
        ("y'", "y"),
        ("y2", "y2"),
    ]

    passed = 0
    failed = 0

    for input_move, expected in test_cases:
        result = mirror_move(input_move)
        status = "✓" if result == expected else "✗"
        if result == expected:
            passed += 1
            print(f"  {status} {input_move:4} → {result:4} (expected {expected})")
        else:
            failed += 1
            print(f"  {status} {input_move:4} → {result:4} (expected {expected}) FAILED!")

    print(f"\nSingle moves: {passed} passed, {failed} failed\n")
    return failed == 0


def test_sequences():
    """Test sequence mirroring"""
    print("=== Sequence Mirror Tests ===\n")

    test_cases = [
        # F2L-01: FR → FL
        ("F R' F' R", "F' L F L'"),
        # F2L-02: FR → FL
        ("R' F R F'", "L F' L' F"),
        # F2L-03: FR → FL
        ("F' U F", "F U' F'"),
        # F2L-04: FR → FL
        ("R U' R'", "L' U L"),
        # F2L-05: FR → FL (more complex)
        ("R U R' U2' R U' R' U", "L' U' L U2' L' U L U'"),
        # With wide moves (R2 → L2, not R2 stays!)
        ("r U' R2 U' R2' U2' r", "l' U L2 U L2' U2' l'"),
        # With M slice (M stays M)
        ("r U2' R' U R U' R' U M", "l' U2' L U' L' U L U' M"),
    ]

    passed = 0
    failed = 0

    for input_seq, expected in test_cases:
        result = mirror_moves(input_seq)
        status = "✓" if result == expected else "✗"
        if result == expected:
            passed += 1
            print(f"  {status} '{input_seq}'")
            print(f"      → '{result}'")
        else:
            failed += 1
            print(f"  {status} '{input_seq}'")
            print(f"      → '{result}'")
            print(f"      expected: '{expected}' FAILED!")
        print()

    print(f"Sequences: {passed} passed, {failed} failed\n")
    return failed == 0


def test_double_mirror():
    """Verify that mirroring twice returns to original"""
    print("=== Double Mirror (Idempotence) Tests ===\n")

    test_moves = ["R", "R'", "R2", "L", "L'", "F", "F'", "U", "U'", "M", "M'", "r", "l'"]

    passed = 0
    failed = 0

    for move in test_moves:
        once = mirror_move(move)
        twice = mirror_move(once)
        status = "✓" if twice == move else "✗"
        if twice == move:
            passed += 1
            print(f"  {status} {move} → {once} → {twice}")
        else:
            failed += 1
            print(f"  {status} {move} → {once} → {twice} (expected {move}) FAILED!")

    print(f"\nDouble mirror: {passed} passed, {failed} failed\n")
    return failed == 0


def test_exhaustive_coverage():
    """Check that all move types have mirror mappings"""
    print("=== Coverage Test ===\n")

    all_moves = [
        # Face moves
        "R", "R'", "R2", "R2'",
        "L", "L'", "L2", "L2'",
        "U", "U'", "U2", "U2'",
        "D", "D'", "D2", "D2'",
        "F", "F'", "F2", "F2'",
        "B", "B'", "B2", "B2'",
        # Wide moves
        "r", "r'", "r2", "r2'",
        "l", "l'", "l2", "l2'",
        "u", "u'", "u2", "u2'",
        "d", "d'", "d2", "d2'",
        "f", "f'", "f2", "f2'",
        "b", "b'", "b2", "b2'",
        # Slice moves
        "M", "M'", "M2", "M2'",
        "E", "E'", "E2", "E2'",
        "S", "S'", "S2", "S2'",
        # Rotations
        "x", "x'", "x2",
        "y", "y'", "y2",
        "z", "z'", "z2",
    ]

    # Moves that correctly map to themselves (symmetric or 180°)
    stays_same = [
        # 180° moves
        "F2", "F2'", "U2", "U2'", "B2", "B2'", "D2", "D2'",
        "f2", "f2'", "u2", "u2'", "b2", "b2'", "d2", "d2'",
        "M2", "M2'", "E2", "E2'", "S2", "S2'",
        "x2", "y2", "z2",
        # M and E are on symmetry axis, stay same
        "M", "M'", "E", "E'",
    ]

    missing = []
    for move in all_moves:
        result = mirror_move(move)
        if result == move and move not in stays_same:
            # These should stay the same (180° moves)
            missing.append(move)

    if missing:
        print(f"  ✗ Missing mirror mappings for: {missing}")
        return False
    else:
        print(f"  ✓ All {len(all_moves)} move types have mirror mappings")
        return True


def main():
    print("=" * 60)
    print("Mirror Logic Verification")
    print("=" * 60)
    print()

    results = []
    results.append(("Single moves", test_single_moves()))
    results.append(("Sequences", test_sequences()))
    results.append(("Double mirror", test_double_mirror()))
    results.append(("Coverage", test_exhaustive_coverage()))

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed!")

    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
