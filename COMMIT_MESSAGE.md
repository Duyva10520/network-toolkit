fix: exclude Python 3.12 on Windows to resolve CI compatibility issues #4

- Excluded Python 3.12 on windows-latest from GitHub Actions test matrix
- Fixed Windows compatibility issues with Python 3.12
- Maintained Python 3.8+ support for all other platforms
- Updated FEATURES.md to document Windows Python 3.12 limitation

This change resolves CI failures while maintaining broad Python version
support across all platforms. Python 3.12 works fine on Linux/macOS.

Fixes: GitHub Actions CI failures with Python 3.12 on Windows