# avfilters

[![Latest Release][pypi-version-badge]][pypi-version-url]
[![Python version][pypi-python-version-badge]][pypi-version-url]
[![Documentation][documentation-badge]][documentation-url]
[![Codecov][codecov-badge]][codecov-url]
[![PDM][pdm-badge]][pdm-url]

Curated list of common Audio/Video filters.

This library wraps the relatively complex PyAV bindings to provide
easy to use audio and video manipulation filters, such as files
concatenation, video reversing or video to GIF.

## Motivation

FFMPEG is a **powerful** tool for media files manipulation. Many
Python libraries already wrap the `ffmpeg` executable to
easily perform audio and video processing in Python.

**However**, most of those libraries call `ffmpeg`
through *subprocesses*. While this is fine in many
use cases, this has two major drawbacks:

1. you must have `ffmpeg` installed on your computer,
   and know the executable path;
2. and repeatedly calling subprocesses in a hot loop can
   be *quite* slow.

For performances reasons, a solution is to use
bindings to the FFMPEG C libraries, e.g.,
[PyAV](https://github.com/PyAV-Org/PyAV). Moreover,
PyAV ships (by default) with pre-built binary wheels
linking against FFMPEG C libraries, so you do not need
to rely on a *possible* local installation of `ffmpeg`.

Unfortunately, using PyAV can be quite complex,
especially as `ffmpeg` usually does a lot of
auto-corrections that PyAV does not automatically
perform.

This library aims at providing a straighforward
`ffmpeg`-like API for some very common use cases.

If you feel like a feature is missing, please
use the
[GitHub issues](https://github.com/jeertmans/avfilters/issues)
and detail your feature request.

## Getting started

First, add `avfilters` to you project's dependencies.

```python
from avfilters import reverse


reverse("original.mp4", "expected.mp4")
```

For more examples, take a look at the documentation.

## Getting help

You have a question or want to report a bug?

Please use the
[GitHub issues](https://github.com/jeertmans/avfilters/issues).

[pypi-version-badge]: https://img.shields.io/pypi/v/avfilters?label=avfilters&color=blueviolet
[pypi-version-url]: https://pypi.org/project/avfilters/
[pypi-python-version-badge]: https://img.shields.io/pypi/pyversions/avfilters?color=orange
[documentation-badge]: https://readthedocs.org/projects/avfilters/badge/?version=latest
[documentation-url]: https://avfilters.readthedocs.io/latest/?badge=latest
[codecov-badge]: https://codecov.io/gh/jeertmans/avfilters/branch/main/graph/badge.svg?token=8P4DY9JCE4
[codecov-url]: https://codecov.io/gh/jeertmans/avfilters
[pdm-badge]: https://img.shields.io/badge/pdm-managed-blueviolet
[pdm-url]: https://pdm-project.org
