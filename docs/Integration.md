## GitHub Workflows
The following Workflow actions are located in `.github/workflows`
>* `push-version.yaml` - runs automatically whenever updates are pushed from remote to repository.
>* `tag-version.yaml` - called by the developer to create a tag.
>* `build-and-publish.yaml` - runs automatically in response to release event, including upload to PyPI.

## VERSION File
### Management
The file at `src/htlfc/VERSION` is managed by workflow actions.

* `tag-version.yaml` will rewrite `VERSION` with a string obtained from `git describe` in the form v0.0.0-N-SHA where v0.0.0 is the last released version, -N is the number of commits since the release and -SHA is GitHub's hash.
* `tag-version.yaml` will rewrite `VERSION` with the string given by the operator, usually the short v0.0.0 form.
* `build-and-publish.yaml` will create a release containing the latest tag (which can only be the short v0.0.0 form).

### Reporting
The VERSION file is reported by `htlfc -v` and embedded into the package name by `setuptools`. Intent of this scheme is that:

* Each released and published package is versioned with the short 'semantic' form v0.0.0
* Any clone or copy, will report either the last release, or the long form if any commits have been made since release.

## Packaging
HTLFC observes PEP517/518. Configuration is held in `pyproject.toml`.
The file `setup.py` contains a stub to enable `setuptools` to create and publish packages.

At build time, `setuptools` will create and install `htlfc` and `htlfc-b` in `$PATH`. At run time, these call `main.main()` and `main.call_browser()` respectively.

