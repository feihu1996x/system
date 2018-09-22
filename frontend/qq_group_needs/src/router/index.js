import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/views/Index'
import FilterKeys from '@/views/FilterKeys'
import FilterQqNumbers from '@/views/FilterQqNumbers'
import FilterGroupNumbers from '@/views/FilterGroupNumbers'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/filter/keys',
      name: "FilterKeys",
      component: FilterKeys
    },
    {
      path: '/filter/qq_numbers',
      name: "FilterQqNumbers",
      component: FilterQqNumbers      
    },
    {
      path: '/filter/group_numbers',
      name: "FilterGroupNumbers",
      component: FilterGroupNumbers      
    }
  ]
})
