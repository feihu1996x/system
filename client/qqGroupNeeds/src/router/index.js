import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/views/Index'
import FilterKeys from '@/views/FilterKeys'
import FilterQqNumbers from '@/views/FilterQqNumbers'
import FilterGroupNumbers from '@/views/FilterGroupNumbers'
import api from "../api";

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: api.ROUTE_PREFIX + '/',
      name: 'Index',
      component: Index
    },
    {
      path: api.ROUTE_PREFIX + '/filter/keys',
      name: "FilterKeys",
      component: FilterKeys
    },
    {
      path: api.ROUTE_PREFIX + '/filter/qq_numbers',
      name: "FilterQqNumbers",
      component: FilterQqNumbers      
    },
    {
      path: api.ROUTE_PREFIX + '/filter/group_numbers',
      name: "FilterGroupNumbers",
      component: FilterGroupNumbers      
    }
  ]
})
