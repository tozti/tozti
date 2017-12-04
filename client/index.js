import App from './components/App.vue'
import Dashboard from './components/Dashboard.vue'

import store from './store'

new Vue({
  el: '#app',

  router: new VueRouter({
    routes: [
      { path: '/', component: Dashboard }
    ]
  }),

  store,
  render: h => h(App)
})

