************
Architecture
************


Tozti serves 3 main HTTP namespaces:

- ``/static``: usual static files (javascript, css, images, etc)
- ``/api``: REST endpoints to interact with the server
- anything else will be responded to with the main ``index.html``


Extensions
==========


The tozti core is really lightweight but it has the ability to load extensions. For now, you only need to know that extension is a folder providing a python file (`server.py`), describing how the extension works on the server (its routes, which files must be included from the client...).
An extension can be installed by pasting its folder inside tozti's `extensions/` folder. During startup, the server will go through every subfolders of `extensions/` and try to load them as an extension.

If you want to know how to create an extension, you can see `the related documentation pages`.

.. _setuptools entrypoint: https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins
.. _the related documentation pages: extensions/index
