************
Architecture
************


Tozti serves 3 main HTTP namespaces:

- ``/static``: usual static files (javascript, css, images, etc)
- ``/api``: REST endpoints to interact with the server
- anything else will be responded to with the main ``index.html``


Extensions
==========

The tozti core is really lightweight but it has the ability to load extensions.
During the startup, the server will search and load any installed python
package that export a `setuptools entrypoint`_ named ``manifest`` in the
``tozti`` group. This entrypoint must map to a dictionary that may contain the
following keys:

``routes``
   This is used to declare new API endpoints. It should be an instance of
   :py:class:`tozti.utils.Router`. More precisely it must have an
   :py:meth:`add_prefix` method and it will be passed to
   :py:meth:`aiohttp.web.UrlDispatcher.add_routes`. Every route declared will
   be prefixed by ``/api/<extension-name>``.

``includes``
   A list of css or js filenames that must be included in the main
   ``index.html``. Usually you will put there your ``main.js`` which contains
   the code to register or patch components.

``_god_mode``
   Beware, this can be dangerous if used incorrectly! This should be a function
   taking as argument the main :py:class:`aiohttp.web.Application` object.
   You can use it to register custom middlewares or do otherwise weird stuff.

``static_dir``
   TODO this is WIP.

.. _setuptools entrypoint: https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins
