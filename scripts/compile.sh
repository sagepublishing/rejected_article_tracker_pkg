###
# Use this script to compile and install locallly
#
# 1. Run this script from project root:
# ```
#   $ scripts/compile.sh
# ```
# 2. use pip to install
# ```
#   $ pip install dist/{{the package you just compiled}}
# ```
##

rm -rf build dist *.egg-info
python3 setup.py bdist_wheel