git tag $(python setup.py --version)

python3 -m twine upload dist/*
git push --tags