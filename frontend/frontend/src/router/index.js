import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import MapView from '../views/MapView.vue'
import Manage from '../views/Manage.vue'
import Login from '../views/Login.vue'
import Look from '../views/Look.vue'
import store from '@/store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Home,
    children: [
      {
        path: '',
        name: 'Home',
        component: MapView
      },
      {
        path: 'manage',
        name: 'Manage',
        component: Manage
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/look',
    name: 'Look',
    component: Look
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/About.vue')
    }
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  const auth = localStorage.getItem('auth')
  if (to.name !== 'Login') {
    if (store.state.auth) {
      next()
    } else if (auth) {
      store.commit('setAuth', JSON.parse(auth))
      next()
    } else {
      next({ name: 'Login' })
    }
  } else {
    next()
  }
})

export default router
