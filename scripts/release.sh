python3 -m twine upload dist/*

if [ $? -eq 0 ]; then
  git tag $(python setup.py --version)
  git push --tags
fi