from tozti.utils import RouterDef
from aiohttp import web


router = RouterDef()
foo = router.add_resource('/foo/{bar}/baz')


@foo.get
async def foo_get(req):
    return web.Response(
        text='you just called /foo/{}/baz'.format(req.match_info['bar']))


MANIFEST = {
    'router': router,
    'includes': ['build.js', 'assets/css/test.css'],
}
