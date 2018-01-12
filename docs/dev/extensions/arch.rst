****************************
Architecture of an extension
****************************

We will describe here how to write a basic extensions. 

An extension is a folder. The name of this folder is the name of the extension. 

Our first extension
===================

Let's create our first extension ! Suppose we call it `<extension-name>`. Create a folder `<extension-name>` and inside it a file `server.py` with the following lines::
    
    MANIFEST = {
    }

Every extension **must** include a `server.py` declaring a dictionnary `MANIFEST`.
Well done, you've just created your first extension !


Hello-world extension
=====================

The previous extension is not doing anything. We will know create an extension that will add one api endpoint. This will allow us to speak about router.

For the moment our `server.py` is empty. To declare new routes, we must import some files::
    
    from tozti.utils import RouterDef
    from aiohttp import web
    from tozti import logger

The first import include an object allowing us to add routes to tozti API. The second import include an object allowing us to create a http request. And the last import import us a logger (something to debug informations).

Then, we create an empty router::

    router = RouterDef()

And we had one endpoint to it. We call it `hello_world` and it will be accessible at the url `<tozti>/api/<extension-name>/hello_world/`::

    hello_world = router.add_resource('/hello_world')

Finally, we define what action our extension should behave when this endpoint is activated. We choose to behave to `get` requests on this endpoint in our example::

    @hello_world.get
    async def hello_world_get(req):
        logger.info("hello world")
        return web.Response(text='Hello world!')

If we wanted to answer to a `post` request, we should have write `@hello_world.post` instead of `@hello_world.get`. 

Unfortunately, for now Tozti doesn't know that the router `router` exists. And that's normal, as we didn't declare it in `MANIFEST`. Remember, `MANIFEST` is the brain of our extension. Everything that an extension defined must be put in the manifest for the server to know of it.

To add the router in the `MANIFEST`, we will modify the declaration of `MANIFEST` such as it is now::
    MANIFEST = {
        'router': router,
    }

Now, when we will be calling `<tozti>/api/<extension-name>/hello_world`, your tozti instance should output a blank web page with the text "Hello world!". And their should also be "hello world" in the logs.


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
