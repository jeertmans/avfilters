"""Common Audio and Video filters.

This package provides an easy-to-use, high-level, and well tested
interface to some of features exposed by the
`av <https://pypi.org/project/av/>`_ module.

While this library was first developed for another Python project,
another Python project,
`Manim Slides <https://github.com/jeertmans/manim-slides>`_,
I welcome any feature suggestion, bug report, or question
in the
`GitHub issues <https://github.com/jeertmans/avfilters/issues>`_!
"""

__all__ = ("__version__", "concatenate", "inspect", "reverse")


from .concatenate import concatenate
from .inspect import inspect
from .reverse import reverse

__version__ = "0.0.1"
