fastlane documentation
----

# Installation

Make sure you have the latest version of the Xcode command line tools installed:

```sh
xcode-select --install
```

For _fastlane_ installation instructions, see [Installing _fastlane_](https://docs.fastlane.tools/#installing-fastlane)

# Available Actions

## iOS

### ios snap

```sh
[bundle exec] fastlane ios snap
```

Alias for screenshots_prod

### ios screenshots_prod

```sh
[bundle exec] fastlane ios screenshots_prod
```

Generate all production screenshots - all devices, all languages

Usage: fastlane screenshots_prod

### ios screenshots_test

```sh
[bundle exec] fastlane ios screenshots_test
```

Quick screenshot test - 1 device, 1 language (English)

Usage: fastlane screenshots_test

### ios frame

```sh
[bundle exec] fastlane ios frame
```

Add device frames to production screenshots

### ios frame_test

```sh
[bundle exec] fastlane ios frame_test
```

Test framing on existing test screenshots

### ios screenshots_dark

```sh
[bundle exec] fastlane ios screenshots_dark
```

Generate dark mode screenshots - all devices, all languages

Usage: fastlane screenshots_dark

### ios screenshots_both

```sh
[bundle exec] fastlane ios screenshots_both
```

Generate both light and dark mode screenshots

Usage: fastlane screenshots_both

### ios screenshots_dark_test

```sh
[bundle exec] fastlane ios screenshots_dark_test
```

Quick dark mode test - 1 device, 1 language

Usage: fastlane screenshots_dark_test

### ios upload_screenshots

```sh
[bundle exec] fastlane ios upload_screenshots
```

Upload screenshots to App Store Connect

### ios test_upload

```sh
[bundle exec] fastlane ios test_upload
```

Test upload - Upload screenshots from screenshots_test directory

### ios screenshots_complete

```sh
[bundle exec] fastlane ios screenshots_complete
```

Complete screenshot workflow: generate + frame

### ios upload_metadata

```sh
[bundle exec] fastlane ios upload_metadata
```

Upload metadata to App Store Connect

### ios upload_release_notes

```sh
[bundle exec] fastlane ios upload_release_notes
```

Upload only release notes to App Store Connect (no screenshots/binary)

### ios upload_all

```sh
[bundle exec] fastlane ios upload_all
```

Upload both screenshots and metadata to App Store Connect

### ios update_release_notes

```sh
[bundle exec] fastlane ios update_release_notes
```

Update all release notes with standard minimal text

Usage: bundle exec fastlane ios update_release_notes

### ios show_version

```sh
[bundle exec] fastlane ios show_version
```

Show current version and build numbers from Xcode project

Usage: bundle exec fastlane ios show_version

### ios bump_patch

```sh
[bundle exec] fastlane ios bump_patch
```

Increment patch version (1.2.3 → 1.2.4)

Usage: bundle exec fastlane ios bump_patch

### ios bump_minor

```sh
[bundle exec] fastlane ios bump_minor
```

Increment minor version (1.2.3 → 1.3.0)

Usage: bundle exec fastlane ios bump_minor

### ios bump_major

```sh
[bundle exec] fastlane ios bump_major
```

Increment major version (1.2.3 → 2.0.0)

Usage: bundle exec fastlane ios bump_major

### ios set_version

```sh
[bundle exec] fastlane ios set_version
```

Set specific version number

Usage: bundle exec fastlane ios set_version version:1.2.3

### ios bump_build

```sh
[bundle exec] fastlane ios bump_build
```

Increment build number

Usage: bundle exec fastlane ios bump_build

### ios commit_version

```sh
[bundle exec] fastlane ios commit_version
```

Commit version changes to git

Usage: bundle exec fastlane ios commit_version

### ios tag_version

```sh
[bundle exec] fastlane ios tag_version
```

Create git tag for current version

Usage: bundle exec fastlane ios tag_version

### ios release_patch

```sh
[bundle exec] fastlane ios release_patch
```

Patch release workflow: bump patch → increment build → commit → tag → create ASC version

Usage: bundle exec fastlane ios release_patch

### ios release_minor

```sh
[bundle exec] fastlane ios release_minor
```

Minor release workflow: bump minor → reset build to 1 → commit → tag → create ASC version

Usage: bundle exec fastlane ios release_minor

### ios release_major

```sh
[bundle exec] fastlane ios release_major
```

Major release workflow: bump major → reset build to 1 → commit → tag → create ASC version

Usage: bundle exec fastlane ios release_major

### ios release_custom

```sh
[bundle exec] fastlane ios release_custom
```

Custom version release workflow: set version → set build → commit → tag → create ASC version

Usage: bundle exec fastlane ios release_custom version:1.2.3 build:42

### ios check_version_status

```sh
[bundle exec] fastlane ios check_version_status
```

Check current App Store Connect version status

Usage: bundle exec fastlane ios check_version_status

### ios create_new_version

```sh
[bundle exec] fastlane ios create_new_version
```

Create a new App Store Connect version

Usage: bundle exec fastlane ios create_new_version version:1.0.7

### ios clean_test

```sh
[bundle exec] fastlane ios clean_test
```

Clean test screenshots

### ios clean_prod

```sh
[bundle exec] fastlane ios clean_prod
```

Clean production screenshots

----

This README.md is auto-generated and will be re-generated every time [_fastlane_](https://fastlane.tools) is run.

More information about _fastlane_ can be found on [fastlane.tools](https://fastlane.tools).

The documentation of _fastlane_ can be found on [docs.fastlane.tools](https://docs.fastlane.tools).
