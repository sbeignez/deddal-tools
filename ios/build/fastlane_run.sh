#!/bin/bash
# Helper script to run fastlane with correct Ruby environment

export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
export PATH="/opt/homebrew/lib/ruby/gems/3.4.0/bin:$PATH"

bundle exec fastlane "$@"
