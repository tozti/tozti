import Hello from './components/Hello.vue';

// add a new route with highest priority
tozti.routes.unshift(
  { path: '/counter', component: Hello }
)
