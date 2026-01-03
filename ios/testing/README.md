# tools/ios/testing - Test Automation

Scripts for running automated tests and validation.

## Overview

This folder contains test automation scripts for the Deddal iOS project.

## Scripts

### test_algorithms.sh

Comprehensive algorithm validation test suite that validates ~300-500 algorithm transformations across F2L, OLL, and PLL cases.

**Usage:**
```bash
./test_algorithms.sh
```

**What it tests:**
- F2L (First Two Layers) algorithm transformations
- OLL (Orientation of Last Layer) algorithm transformations
- PLL (Permutation of Last Layer) algorithm transformations
- Algorithm correctness (scramble → solution → solved state)
- Edge cases and corner cases

**How it works:**
1. Temporarily enables disabled tests in `DeddalTests/CaseAlgsTests.swift`
2. Runs `xcodebuild test` with the algorithm test suite
3. Validates all algorithm transformations
4. Restores test file to original state
5. Outputs test results and coverage report

**Integration:**
- **GitHub Actions**: Used by `.github/workflows/test_algorithms.yml`
  - Runs on PRs when algorithm files change
  - Runs on push to main
  - Provides automated validation before merge

**CI/CD Workflow:**
```yaml
# Triggered on:
- pull_request (paths: Deddal/Models/Methods/**, Deddal/Models/Cube/**)
- push to main
- workflow_dispatch (manual)
```

**Output:**
- Test summary (passed/failed counts)
- Individual test results
- Code coverage report
- Test execution log

**Test destination:**
- Simulator: iPhone 17 Pro
- Platform: iOS Simulator
- Configuration: Debug (1. DEV Scheme)

## Running Tests Manually

### Run algorithm tests directly via xcodebuild:

```bash
# Run all algorithm tests
xcodebuild test \
  -project Deddal.xcodeproj \
  -scheme "1. DEV Scheme" \
  -only-testing:DeddalTests/CaseAlgsTests \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro'
```

### Run specific test methods:

```bash
# Test F2L algorithms only
xcodebuild test \
  -project Deddal.xcodeproj \
  -scheme "1. DEV Scheme" \
  -only-testing:DeddalTests/CaseAlgsTests/testF2LAlgorithms \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro'
```

### Run full test suite:

```bash
# All tests (all test classes)
xcodebuild test \
  -project Deddal.xcodeproj \
  -scheme "1. DEV Scheme" \
  -testPlan Deddal.xctestplan \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro'
```

## Test Coverage

The algorithm validation tests cover:

### F2L Cases (42 cases × 2 orientations = 84 tests)
- All 42 F2L pair configurations
- Both FL (Front-Left) and FR (Front-Right) orientations
- Scramble → algorithm → solved validation

### OLL Cases (57 tests)
- All 57 OLL cases
- Last layer orientation validation
- Cross, edges, and corners verification

### PLL Cases (21 tests)
- All 21 PLL cases
- Last layer permutation validation
- Corner and edge permutation correctness

**Total:** ~300-500 algorithm transformation validations

## Test Files

- **Test Suite**: `DeddalTests/CaseAlgsTests.swift`
  - Uses Swift Testing framework (not XCTest)
  - Tests disabled by default with `.disabled()` modifier
  - Enabled temporarily by `test_algorithms.sh` for CI/CD

- **Test Plan**: `Deddal.xctestplan`
  - Defines test configurations
  - Includes all test targets

- **Model Files** (tested):
  - `Deddal/Models/Methods/MethodCase.swift`
  - `Deddal/Models/Methods/Algorithm.swift`
  - `Deddal/Models/Methods/MethodLibrary.swift`
  - `Deddal/Models/Cube/FacesCube.swift`
  - `Deddal/Models/Cube/CubieCube.swift`

## GitHub Actions Integration

The `test_algorithms.sh` script is used by the GitHub Actions workflow:

**Workflow file:** `.github/workflows/test_algorithms.yml`

**Trigger paths:**
- `Deddal/Models/Methods/**`
- `Deddal/Models/Cube/**`
- `DeddalTests/CaseAlgsTests.swift`
- `tools/ios/testing/test_algorithms.sh`

**Actions:**
1. Checkout repository
2. Setup Xcode (latest stable)
3. List available simulators
4. Run `test_algorithms.sh`
5. Process test results
6. Upload test artifacts (results + coverage)
7. Generate coverage report
8. Comment results on PR (if applicable)

**Artifacts:**
- `algorithm-test-results` (TestResults.xcresult + test_output.log)
- `algorithm-coverage-report` (coverage_report.txt)
- Retention: 30 days

## Common Workflows

### Before Committing Algorithm Changes

Run tests locally to catch issues early:
```bash
cd tools/ios/testing
./test_algorithms.sh
```

Review output for failures before pushing.

### Debugging Test Failures

1. **Run specific test**:
   ```bash
   xcodebuild test \
     -project Deddal.xcodeproj \
     -scheme "1. DEV Scheme" \
     -only-testing:DeddalTests/CaseAlgsTests/testOLLCase_01 \
     -destination 'platform=iOS Simulator,name=iPhone 17 Pro'
   ```

2. **Review test implementation** in `DeddalTests/CaseAlgsTests.swift`

3. **Check algorithm definition** in `Deddal/Models/Methods/`

4. **Validate cube transformations** manually or with debugger

### CI/CD Monitoring

After pushing changes:
1. Check GitHub Actions tab for workflow status
2. Review test results in workflow logs
3. Download artifacts if tests fail
4. Review PR comments for test summary

## Dependencies

**Required tools:**
- Xcode 17+ (with command-line tools)
- xcodebuild (included with Xcode)
- xcrun (included with Xcode)
- iOS 18+ Simulator

**Simulator setup:**
```bash
# List available simulators
xcrun simctl list devices available

# Ensure iPhone 17 Pro is available (or update test_algorithms.sh)
```

## Related Documentation

- Main testing guide: `/documentation/04-testing/AI_TESTING_STRATEGY.md`
- Test implementation: `DeddalTests/CaseAlgsTests.swift`
- Algorithm models: `Deddal/Models/Methods/`
- Cube models: `Deddal/Models/Cube/`
- CI/CD workflow: `.github/workflows/test_algorithms.yml`

## Troubleshooting

**Tests fail locally but pass in CI:**
- Check Xcode version matches CI (latest stable)
- Verify simulator configuration
- Clean build folder: `xcodebuild clean`
- Restart Xcode and simulators

**Simulator not found:**
- Update destination in `test_algorithms.sh` to match available simulators
- Run `xcrun simctl list devices available` to see options
- Install required simulator in Xcode preferences

**Permission errors:**
- Make script executable: `chmod +x test_algorithms.sh`
- Check file permissions in git

**Test timeouts:**
- Increase timeout in `test_algorithms.sh` (default: 30 minutes)
- Check for infinite loops in test cases
- Review algorithm complexity

**Coverage report issues:**
- Ensure test run completed successfully
- Check `TestResults.xcresult` exists
- Verify xccov is available: `xcrun xccov --version`

Generated by Trophee Ltd
