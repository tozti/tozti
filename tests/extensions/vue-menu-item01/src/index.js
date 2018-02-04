tozti.routes.unshift(
    {path: '/foo', component:
        Vue.component("foo", {template: "<p>success</p>"})
    }
)
tozti.addMenuItem("test menu item", "/foo")
