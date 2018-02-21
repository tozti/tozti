import ToztiLayout from './components/Tozti.vue'

import LoginView from './components/Login.vue'
import SignUpView from './components/SignUp.vue'

import Workspaces from './components/views/Workspaces.vue'
import Groups from './components/views/Groups.vue'
import GroupView from './components/views/Group.vue'
import SettingsView from './components/views/Settings.vue'


const singleRoutes =
  [ { path: '/login'
    , component: LoginView
    , meta: { requiresNoAuth: true }
    }

  , { path: '/signup'
    , component: SignUpView
    , meta: { requiresNoAuth: true }
    }
  ]


const enclosedRoutes =
  [ { path: 'g/', component: Groups }

  , { name: 'group'
    , path: 'g/:id'
    , component: GroupView
    , props: true
    }

  , { path: 'settings', component: SettingsView }

  , { path: 'w/', component: Workspaces }
  ]


/**
 * @param {Route[]} routes - The routes to add.
 */
export function addRoutes(routes) {
  routes.forEach(route => {
    if (route.meta && route.meta.single) {
      singleRoutes.push(route)
    }
    else {
      enclosedRoutes.push(route)
    }
  })
}


export function getRoutes() {
  return singleRoutes.concat([
    { path: ''
    , component: ToztiLayout
    , meta: { requiresAuth: true }
    , redirect: 'g/'
    , readonly: true
    , children: enclosedRoutes
    }
  ])
}
