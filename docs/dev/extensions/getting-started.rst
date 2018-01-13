***************
Getting Started
***************

Our first extension
===================

Let's see how to create a simple extension to *tozti*.
Everything defined by an extension lives inside the same folder, whose name is the name of the extension.

Suppose we call it ``extension-name``. Browse to the ``extensions/`` folder and proceed to create a folder ``extension-name``.
The only requirement for *tozti* to recognize an extension is for this extension to provide a file ``server.py`` declaring a dictionnary ``MANIFEST``.
Thus a minimal definition would like like so::

    MANIFEST = {}

Well done, you've just created your first extension!


Defining an API endpoint
========================

The previous extension currently does nothing. We will now see how to add new API endpoints to the application.

For the moment our ``MANIFEST`` is empty. To declare new routes, we must import some modules::

    from tozti.utils import RouterDef
    from aiohttp import web
    from tozti import logger

- ``RouterDef`` allows us to define a new router and therefore new request handlers.
- ``web`` from ``aiohttp`` enables us to send back to the user simple responses.
- ``logger`` is a simple utility to pretty print information in the server logs.

Then, we create an empty router::

    router = RouterDef()

And we add one endpoint to it. We call it ``hello_world``, and make it accessible from the URL ``<tozti>/api/extension-name/hello_world``::

    hello_world = router.add_resource('/hello_world')

Finally, we define how our extension should behave when this endpoint is requested. In this example, we respond to ``GET`` requests on this endpoint with some dummy text::

    @hello_world.get
    async def hello_world_get(req):
        logger.info("hello world")
        return web.Response(text='Hello world!')

Similar decorators are available for the usual HTTP methods: ``@hello_world.post``, etc.

Unfortunately, for now *tozti* still isn't aware of this new request handler we just defined. This is where ``MANIFEST`` comes to use: We simply add the router in the ``MANIFEST`` dict under the key ``router``::

    MANIFEST = {
        'router': router,
    }

In fact, ``MANIFEST`` is where we declare anything that *tozti* should be made aware of.

And now, if you launch the server again, and visit the URL ``<tozti>/api/extension-name/hello_world``, your browser should display a blank web page with the text *"Hello world!"*. If you look in the server logs, some ``hello world`` must have appeared.


Using Vue.js inside of your extension
=====================================

You will probably want to be able to add some javascript to your extension, so that it can add a page to your website. As we chose to work with `vue.js`, I will explain here how to use it in an extension.

Remember,`vue.js`works with `npm`. So we will add a `package.json` file inside `<extension-name>/` to deal with npm's packages. You can also add a `webpack.config.js` file if you wanted to. In the end, most of the time you will want to add a javascript file` to the static pages of tozti (or/and a CSS page). This is to what corresponds the key `includes` inside the `MANIFEST` dictionary.
For example, adding `includes=['build.js', 'assets/css/test.css']` will allow tozti to link the corresponding files inside of its `index.html`

A concrete example of a small `vue js` extension of tozti is disponible inside the repository (TODO: add repository name, I will do it later)


**Warning**
As vue.js uses the npm ecosystem, chances are that you need to do some actions (like compile) on some files before generating a `build.js` file (or whatever). Make sure to execute these commands before installing/updating the extensions, otherwise it will not work correctly. 


Going further with MANIFEST
===========================

Here are a complete list of keys that `MANIFEST` can possess:
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

``dependencies``
    A list of names of extensions that must be loaded before this extension in 
    order for it to be working as intended.


MANIFEST = {
    'router': router,
    'includes': ['build.js', 'assets/css/test.css'],
}
