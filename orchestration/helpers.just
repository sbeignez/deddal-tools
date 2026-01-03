# Reusable helper recipes

# Print colored success message
_success msg:
    @echo -e "{{COLOR_GREEN}}✅ {{msg}}{{COLOR_RESET}}"

# Print colored warning message
_warn msg:
    @echo -e "{{COLOR_YELLOW}}⚠️  {{msg}}{{COLOR_RESET}}"

# Print colored error message and exit
_error msg:
    @echo -e "{{COLOR_RED}}❌ {{msg}}{{COLOR_RESET}}" && exit 1

# Print colored info message
_info msg:
    @echo -e "{{COLOR_BLUE}}ℹ️  {{msg}}{{COLOR_RESET}}"

# Print colored step message
_step num total msg:
    @echo -e "{{COLOR_CYAN}}[{{num}}/{{total}}] {{msg}}{{COLOR_RESET}}"

# Execute a script with error handling
_exec script *args:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -f "{{script}}" ]; then
        echo -e "{{COLOR_RED}}❌ Script not found: {{script}}{{COLOR_RESET}}"
        exit 1
    fi
    chmod +x "{{script}}"
    if ! "{{script}}" {{args}}; then
        echo -e "{{COLOR_RED}}❌ Failed: {{script}}{{COLOR_RESET}}"
        exit 1
    fi

# Confirm action (Y/n)
_confirm prompt:
    #!/usr/bin/env bash
    echo -n "{{prompt}} (Y/n) "
    read -r response
    response="$(printf '%s' "$response" | tr -d '[:space:]')"
    if [[ -n "$response" && ! "$response" =~ ^([yY]|[yY][eE][sS])$ ]]; then
        echo -e "{{COLOR_YELLOW}}⚠️  Cancelled{{COLOR_RESET}}"
        exit 1
    fi

# Check if Python venv exists in directory
_check-venv dir:
    #!/usr/bin/env bash
    if [ ! -d "{{dir}}/venv" ]; then
        echo -e "{{COLOR_RED}}❌ Python venv not found in {{dir}}{{COLOR_RESET}}"
        echo -e "{{COLOR_YELLOW}}Run: just setup-python-env{{COLOR_RESET}}"
        exit 1
    fi

# Run Python script with venv activation
_python-exec dir script *args:
    #!/usr/bin/env bash
    set -euo pipefail
    just _check-venv "{{dir}}"
    cd "{{dir}}"
    source venv/bin/activate
    {{PYTHON}} "{{script}}" {{args}}

# Run xcodebuild with common settings
_xcodebuild-run scheme config action:
    xcodebuild \
        -project {{XCODE_PROJECT}} \
        -scheme "{{scheme}}" \
        -configuration {{config}} \
        {{action}}

# Run xcodebuild test with simulator
_xcodebuild-test scheme testplan destination:
    xcodebuild test \
        -project {{XCODE_PROJECT}} \
        -scheme "{{scheme}}" \
        -testPlan {{testplan}} \
        -destination "{{destination}}"

# Print a divider line
_divider:
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
