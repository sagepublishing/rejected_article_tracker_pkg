import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='rejected_article_tracker',
    version='1.5.13',
    scripts=['rejected_article_tracker/__init__.py'],
    author="Andy Hails",
    author_email="andy.hails@sagepub.co.uk",
    description="Utility package to track if a journal article has been published somewhere.",
    long_description='',#long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sagepublishing/rejected_article_tracker_pkg",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['rejected_article_tracker/src/ML/small_models/lr_model',
                        'rejected_article_tracker/data/fake_rejected_articles.xlsx']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'scikit-learn==1.0.2',
        'markdown',
        'pandas',
        'openpyxl',
        'xlsxwriter',
        'fuzzywuzzy',
        'requests',
        'oaiharvest',
        'langdetect',
        'gensim',
        
        'numpy',
        'python-Levenshtein',
        'tqdm',
        'xmltodict'
    ],
)
