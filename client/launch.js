import Vue from 'vue'
import Buefy from 'buefy'
import tozti from 'tozti'

Vue.use(Buefy)

const app = window.app = new Vue({
  el: '#app',

  store: tozti.store,

  router: new VueRouter({
    mode: "history",
    routes: tozti.routes
  }),

  render: h => h(tozti.App)
})

// we still want to give the possibility for modules
// to have some control over the final app component
tozti.postLaunchHooks.forEach(hook => hook(app))
