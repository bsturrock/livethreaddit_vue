import { resolveDirective } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import LiveThread from '../views/LiveThread.vue'
import Redirect from '../views/Redirect.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/r/:subreddit/comments/:threadid/:temptitle/',
    name: 'LiveThread',
    component: LiveThread,
    props: true,
  },
  {
    path:'/redirect',
    name: 'Redirect',
    component: Redirect,
  }
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
