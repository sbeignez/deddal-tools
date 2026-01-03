# Testing Recipes
# Prefix: test-*

# Validate seed data JSON files (no DB required)
test-seed-data:
    @just _info "🧪 Validating seed data..."
    @{{SEED_DIR}}/venv/bin/python {{SEED_DIR}}/scripts/ci_validate.py --verbose
    @just _success "Seed data validation passed"

# Run algorithm validation tests (~300-500 cases)
test-algorithms:
    @just _info "🧪 Running algorithm validation tests..."
    @just _exec {{TESTING_DIR}}/test_algorithms.sh
    @just _success "Algorithm tests passed"

# Run algorithm tests for specific method (f2l, oll, pll)
test-algorithms-method method:
    @just _info "🧪 Running {{method}} algorithm tests..."
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{TESTING_DIR}}
    METHOD={{method}} ./test_algorithms.sh
    just _success "{{method}} algorithm tests passed"
