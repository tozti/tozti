import LoginView from './components/Login.vue'
import SignUpView from './components/SignUp.vue'
import ToztiLayout from './components/Tozti.vue'
import DashboardView from './components/views/Dashboard.vue'
import SummaryView from './components/views/Summary.vue'
import TaxonomyView from './components/views/Taxonomy.vue'

import Workspaces from './components/views/Workspaces.vue'
import Groups from './components/views/Groups.vue'
import GroupView from './components/views/Group.vue'

// the readonly tag is present and express the fact 
// that this route mustn't be modified
let routes =
  [ { path: '/login'
    , component: LoginView
    , readonly: true
    , meta: { requiresNoAuth: true }
    },
    { path: '/signup'
    , component: SignUpView
    , readonly: true
    , meta: { requiresNoAuth: true }
    },
    { path: ''
    , component: ToztiLayout
    , meta: { requiresAuth: true }
    , redirect: 'g/'
    , readonly: true
    , children:
        [ { path: 'g/', component: Groups }
         //, { path: 'foo/', component: Groups}
        , { path: 'g/:id', name: 'group', component: GroupView
          , props: route => ({ id: route.params.id }) }
        , { path: 'w/', component: Workspaces }
        , { path: 'w/:id',  name: 'workspace', component: SummaryView }
        , { path: 'w/:taxonomy+', component: TaxonomyView, props: true }
        ]
    }
  ]

export default routes
