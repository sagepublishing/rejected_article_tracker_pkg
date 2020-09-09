rm -rf build dist rejected_article_tracker.egg-info
python setup.py bdist_wheel
pip install dist/rejected_article_tracker-0.41-py3-none-any.whl
