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

``router``
   This is used to declare new API endpoints. It should be an instance of
   :py:class:`tozti.utils.RouterDef`. More precisely it must have an
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
   The directory containing static resources (relatively to the distribution
   root, ie the directory containing the ``setup.py``). Note that this is only
   used in dev mode when the extension is installed in ``develop`` (``-e``)
   mode.

The extension should install it's static file in
``<prefix>/share/tozti/<extension-name>`` (where ``<prefix>`` is the python
installation prefix). To do that use the ``data_files`` argument in the
``setup.py``.

Example
-------

A sample extension exporting a single endpoint and a js file named could look
like this::

   # setup.py
   from setuptools import setup

   setup(
       'myext',
       py_modules=[
           'myext'
       ],
       install_requires=[
           'tozti',
           'aiohttp',
       ],
       data_files=[
           ('share/tozti/myext', ['dist/main.js']),
       ],
       entrypoints={
          'tozti': ['manifest = myext:MANIFEST']
       },
   )

::

   # myext.py
   from tozti.utils import RouterDef
   from aiohttp.web import Response

   router = RouterDef()
   foo = router.add_resource('/foo/{name}')

   @foo.get
   def handle_get(req):
       return Response(text='Your name is {}'.format(req.match_info['name']))

   MANIFEST = {
       'router': router,
       'includes': ['main.js'],
       'static_dir': 'dist',
   }

::

   # dist/main.js
   window.alert("tozti-ext/main.js has been loaded!")

To activate the extension, simply install it in the same venv as tozti, and it
will get detected. The ``main.js`` file will be hosted at the URL
``/static/myext/main.js`` and the endpoint will be at
``/api/myext/foo``. Because of the ``includes`` line, an alert will be
displayed each time we load the ``index.html`` (if it had been an empty line,
the file would still be hosted at the same URL but it wouldn't have been loaded
in the ``index.html``).

.. _setuptools entrypoint: https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins
