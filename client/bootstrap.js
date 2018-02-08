import Buefy from 'buefy'

import App       from './components/App.vue'
import Dashboard from './components/Dashboard.vue'
import Taxonomy  from './components/Taxonomy.vue'
import Summary from './components/Summary.vue'

import store from './store'
import api from './api'

Vue.use(Buefy)

// Create a 'polymorphic' component.
// A polymorphic component is a component with a single prop `resource` that
// transparently passes the rendering to another component based on the type
// of the passed resource. To register a new component handling a given type,
// add the instance as a property of the returned object.
//
// Example: make a 'thumbnail' component
//
//   let thumb_tbl = polymorphic_component('thumbnail', {
//       template: '<p>Thumbnail for {{resource.id}}</p>',
//       props: ['resource'],
//   });
//   thumb_tbl['image'] = {
//       template: '<p>Thumbnail for image {{resource.id}}'</p>,
//       props: ['resource'],
//   };
//   thumb_tbl['thread'] = {
//       template: '<p>Thumbnail for thread {{resource.id}}</p>',
//       props: ['resource'],
//   };

// TODO(flupe): move this to a more appropriate place
//              i mean, come on Lapin0t

export function polymorphic_component(name, fallback) {
    let table = {fallback: fallback};
    Vue.component(name, {
        template: '<component :is="sub" :resource="resource"/>',
        props: ['resource'],
        computed: {
            sub() {
                return table[this.resource.type] || table['fallback'];
            }
        }
    });
    return table;
}

export let tozti = window.tozti = {
  store,
  api,

  App,

  routes: [
    { name: 'home',      path: '/',      component: Dashboard },
    { name: 'workspace', path: '/w/:id', component: Summary },
    { path: '/w/:taxonomy+', component: Taxonomy },
  ],

  globalMenuItems: [
    { name: 'Accueil', route: '/', props: { icon: 'nc-home-52' } }
  ],

  workspaceMenuItems: [
    { name: 'Résumé', route: 'workspace', props: { icon: 'nc-grid-45' } }
  ],

  /**
   * Define a global sidebar menu item.
   * @param {string} name - The name of the menu item.
   * @param {string | Location} route - The route it points to.
   */
  addMenuItem(name, route, props = {}) {
    tozti.globalMenuItems.push({ name, route, props})
  },

  /**
   * @param {string} name  - The name of the workspace menu item.
   * @param {string} route - The name of the route it is associated with.
   *                         This route should expect an id as a parameter.
   */
  addWorkspaceMenuItem(name, route, props = {}) {
    tozti.workspaceMenuItems.push({ name, route, props })
  },

  postLaunchHooks: [],
}

