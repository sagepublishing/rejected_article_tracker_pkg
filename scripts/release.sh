###
# Use this script to release to pypi.
# 1. Update version in setup.up
# 2. COMMIT everything
# 3. Run this script from project root:
# ```
#   $ scripts/release.sh
# ```
##
git tag $(python setup.py --version)
git push --tags