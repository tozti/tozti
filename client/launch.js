const app = window.app = new Vue({
  el: '#app',

  store: tozti.store,

  router: new VueRouter({
    routes: tozti.routes
  }),

  render: h => h(tozti.components.App)
})

// we still want to give the possibility for modules
// to have some control over the final app component
tozti.postLaunchHooks.forEach(hook => hook(app))
