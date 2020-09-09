

Prerequisites:

```
pip install --upgrade pip setuptools wheel
pip install tqdm
pip install --user --upgrade twine
```

To compile:
```
python setup.py bdist_wheel
```

To push to pypi:
```
python -m twine upload dist/*
```
