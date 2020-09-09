## Usage
```
from rejected_article_tracker import RejectedArticlesMatch

results = []
RejectedArticlesMatch(
            articles=articles,
            config=config,
            email=email,
            results=results
        ).match()
```

<br>
<br>

---
## Compile and deploy  

Prerequisites:

```
pip install --upgrade pip setuptools wheel
pip install tqdm
pip install --user --upgrade twine
```

To compile:
```
python3 setup.py bdist_wheel
```

To push to pypi:
```
python3 -m twine upload dist/*
```
