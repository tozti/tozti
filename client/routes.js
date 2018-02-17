import LoginView from './components/Login.vue'
import SignUpView from './components/SignUp.vue'
import ToztiLayout from './components/Tozti.vue'
import DashboardView from './components/views/Dashboard.vue'
import SummaryView from './components/views/Summary.vue'
import TaxonomyView from './components/views/Taxonomy.vue'

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
    , children:
        [ { path: '',      component: DashboardView }
        , { path: 'w/:id',  name: 'workspace', component: SummaryView }
        , { path: 'w/:taxonomy+', component: TaxonomyView, props: true }
        ]
    }
  ]

export default routes
