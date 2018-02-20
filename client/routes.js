import LoginView from './components/Login.vue'
import SignUpView from './components/SignUp.vue'
import ToztiLayout from './components/Tozti.vue'
import DashboardView from './components/views/Dashboard.vue'
import SummaryView from './components/views/Summary.vue'
import TaxonomyView from './components/views/Taxonomy.vue'

import Workspaces from './components/views/Workspaces.vue'
import Groups from './components/views/Groups.vue'

const routes =
  [ { path: '/login'
    , component: LoginView
    , meta: { requiresNoAuth: true }
    },
    { path: '/signup'
    , component: SignUpView
    , meta: { requiresNoAuth: true }
    }
  , { path: ''
    , component: ToztiLayout
    , meta: { requiresAuth: true }
    , redirect: 'g/'
    , children:
        [ { path: 'g/', component: Groups }
        , { path: 'g/:handle', name: 'group', component: Groups }
        , { path: 'w/', component: Workspaces }
        , { path: 'w/:id',  name: 'workspace', component: SummaryView }
        , { path: 'w/:taxonomy+', component: TaxonomyView, props: true }
        ]
    }
  ]

export default routes
