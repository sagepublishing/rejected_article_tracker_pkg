# Contributing
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [Code of Conduct](CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.


## Notes for deployment 

Prerequisite - tools to be installed 

```
pip install --upgrade pip setuptools wheel
pip install tqdm
pip install --user --upgrade twine
```

**To compile for local development:**
```
scripts/compile.sh
```

**To push to pypi:**
The GitHub CI takes care of compilation and deployment to pypi.
 
You just need to the following to deploy:
1. Update version in [`setup.py`](setup.py) 
2. Commit your code.
2. Run the release script from the root of this project:

```
$ scripts/release.sh
```