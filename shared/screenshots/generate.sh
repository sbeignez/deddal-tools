#!/bin/bash
# Screenshot Automation System - Main Entry Point
# Orchestrates the entire screenshot generation pipeline

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source colors
source "${SCRIPT_DIR}/scripts/lib/colors.sh"

# Print header
print_header() {
    echo -e "\n${MAGENTA}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║${NC}  ${WHITE}Screenshot Automation System${NC}                            ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}║${NC}  Fast, reliable, Fastlane-free screenshot generation   ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════╝${NC}\n"
}

# Print usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

OPTIONS:
    -h, --help          Show this help message
    -c, --capture-only  Only run Step 1 (capture screenshots)
    -f, --frame-only    Run Steps 2-4 (add bezel, background, text)
    -u, --upload-only   Only run Step 5 (upload screenshots)
    -d, --debug         Enable debug output

EXAMPLES:
    # Full pipeline (capture -> bezel -> background -> text -> upload)
    $0

    # Capture only
    $0 --capture-only

    # Frame existing screenshots (bezel -> background -> text)
    $0 --frame-only

    # Debug mode
    DEBUG=1 $0

EOF
}

# Main pipeline
main() {
    local run_capture=true
    local run_frame=true
    local run_upload=true

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            -c|--capture-only)
                run_frame=false
                run_upload=false
                shift
                ;;
            -f|--frame-only)
                run_capture=false
                run_upload=false
                shift
                ;;
            -u|--upload-only)
                run_capture=false
                run_frame=false
                shift
                ;;
            -d|--debug)
                export DEBUG=1
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done

    print_header

    local start_time=$(date +%s)

    # Step 1: Capture Screenshots
    if [ "${run_capture}" = true ]; then
        "${SCRIPT_DIR}/scripts/1_snap.sh" || {
            log_error "Screenshot capture failed"
            exit 1
        }
    fi

    # Step 2: Add Device Bezels
    if [ "${run_frame}" = true ]; then
        "${SCRIPT_DIR}/scripts/2_frame.sh" || {
            log_error "Adding bezels failed"
            exit 1
        }
    fi

    # Step 3: Add Gradient Backgrounds
    if [ "${run_frame}" = true ]; then
        "${SCRIPT_DIR}/scripts/3_background.sh" || {
            log_error "Adding backgrounds failed"
            exit 1
        }
    fi

    # Step 4: Add Text Overlays
    if [ "${run_frame}" = true ]; then
        "${SCRIPT_DIR}/scripts/4_text.sh" || {
            log_error "Adding text overlays failed"
            exit 1
        }
    fi

    # Step 5: Upload to App Store
    if [ "${run_upload}" = true ]; then
        "${SCRIPT_DIR}/scripts/5_upload.sh" || {
            log_error "Screenshot upload failed"
            exit 1
        }
    fi

    # Calculate duration
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    local minutes=$((duration / 60))
    local seconds=$((duration % 60))

    echo ""
    log_success "All done! ✨"
    log_info "Total time: ${minutes}m ${seconds}s"
    echo ""
}

# Run main function
main "$@"
