*******************
Tozti documentation
*******************

This repo hold the documentation for the Tozti project. It is built using
`sphinx`_ and can be seen online at `readthedocs`_.

Editing
=======

The documentation is written in *reStructuredText* (reST) markup which is
somewhat similar to markdown, but way more powerful. Take a look at the
`cheatsheet`_ or the `specification`_ for informations on how to use reST.

Installing Sphinx
=================

The Sphinx package is available on the PyPI, you can install it with the usual
``pip --user install sphinx``. If you have multiple python versions installed
replace ``pip`` with ``python3 -m pip``; if you don't have pip
installed on that python version, just run ``python3 -m ensurepip`` first.

Building
========

Just issue ``make html`` inside the ``docs`` directory. The output will be
inside ``docs/_build/html``, you can view it locally by running ``python3 -m
http.server 8080`` and browsing http://localhost:8080. Do *not* include
output files in the repository, the documentation is being built automatically
by readthedocs.


.. _readthedocs: https://tozti.readthedocs.io/en/latest
.. _sphinx: http://www.sphinx-doc.org/en/stable/
.. _cheatsheet: http://www.sphinx-doc.org/en/stable/rest.html
.. _specification: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
