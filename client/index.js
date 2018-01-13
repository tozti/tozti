import App       from './components/App.vue'
import Dashboard from './components/Dashboard.vue'
import Taxonomy  from './components/Taxonomy.vue'

import store from './store'

window.tozti = new Vue({
  el: '#app',
  store,

  router: new VueRouter({
    routes: [
      { path: '/', component: Dashboard },
      { path: '/:workspace/:taxonomy*', component: Taxonomy }
    ]
  }),

  render: h => h(App)
})
