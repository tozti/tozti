import App       from './components/App.vue'
import Dashboard from './components/Dashboard.vue'
import Taxonomy  from './components/Taxonomy.vue'

import store from './store'

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

const tozti = window.tozti = {
  store,

  // TODO(flupe): find a ES6-y way of making tozti components available to plugins
  // I think this should be doable in an easy way
  // probably just need to dive in the browserify documentation
  components: { App, Dashboard, Taxonomy },

  routes: [
    { path: '/', component: Dashboard },
    { path: '/:workspace/:taxonomy*',
      component: Taxonomy,

      // TODO(flupe):
      //   - define the validation behavior
      //     and how it should interact with tozti.store
      //   - find a nice way to define this alongside the Taxonomy component
      beforeEnter: (to, from, next) => {
        // validation 1:
        //   can we access this workspace?

        // validation 2:
        //   can we access this subpath?

        // if everything is ok, then
        next()
      }
    }
  ],

  globalMenuItems: [
    { name: 'Accueil', route: 'counter', props: { } } 
  ],

  /**
   * @param {string} name - The name of the menu item.
   * @param {string | Location} route - The route it points to.
   */
  addMenuItem(name, route, props = {}) {
    tozti.globalMenuItems.push({ name, route, props})
  },

  postLaunchHooks: []
}

export default tozti
