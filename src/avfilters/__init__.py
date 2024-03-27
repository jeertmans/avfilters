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

Install
-------

All you need is to add ``avfilters`` to your list of dependencies.

On most modern platforms, it will download binary wheels so you do
not need to worry about a local FFmpeg installation. However,
if your platform does not have pre-built binary wheels, or if you
want to use an already existing FFmpeg installation, please
checkout
`PyAV's installation instructions <https://pyav.org/docs/stable/overview/installation.html>`_.

Usage
-----

Using this library should be *straightforward*, as most
functions contain a well-defined, self-contained, feature.

E.g., if you want to reverse a media, then just use
:func:`avfilters.reverse`.

For more usage examples, please see the documentation of
each individual function.

Re-exports
----------

The core utilities of this library are re-exported
in the main module. For more details or functionalities,
check individual submodules.
"""

__all__ = ("__version__", "concatenate", "inspect", "reverse")


from .concatenate import concatenate
from .inspect import inspect
from .reverse import reverse

__version__ = "0.0.1"
