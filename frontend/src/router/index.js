import { createRouter, createWebHistory } from 'vue-router'
import StrategyList from '../views/strategy/StrategyList.vue'

const routes = [
  {
    path: '/',
    redirect: '/strategy'
  },
  {
    path: '/strategy',
    name: 'StrategyList',
    component: StrategyList
  },
  {
    path: '/strategy/create',
    name: 'StrategyCreate',
    component: () => import('../views/strategy/StrategyEdit.vue')
  },
  {
    path: '/strategy/edit/:id',
    name: 'StrategyEdit',
    component: () => import('../views/strategy/StrategyEdit.vue')
  },
  {
    path: '/strategy/test/:id',
    name: 'StrategyTest',
    component: () => import('../views/strategy/StrategyTest.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 