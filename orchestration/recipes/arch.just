# Architecture validation recipes

arch-check:
	@just _info "Running architecture dependency checks..."
	@./tool-arch/check_dependencies.sh
	@just _success "Architecture checks passed"

arch-check-layer layer:
	@just _info "Running architecture checks for {{layer}}..."
	@rg "import SwiftUI" "{{layer}}" && { echo "SwiftUI found in {{layer}}"; exit 1; } || true
	@just _success "{{layer}} validation passed"
