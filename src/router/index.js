import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import LiveThread from '../views/LiveThread.vue'

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
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
