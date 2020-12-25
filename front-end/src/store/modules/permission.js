import {adminRoutes, constantRoutes} from '@/router'
import Layout from "@/layout/index";
import {getPluginInfos} from '@/api/plugin'
import {getLanguage} from "@/lang";

/**
 * Use meta.role to determine if the current user has permission
 * @param roles
 * @param route
 */
function hasPermission(roles, route) {
  if (route.meta && route.meta.roles) {
    return roles.some(role => route.meta.roles.includes(role))
  } else {
    return true
  }
}
function getAdminRouter() {
  return adminRoutes
}
const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  generateRoutes({commit}, roles) {
    return new Promise(resolve => {
      let accessedRoutes = []
      let pluginRoutes = []
      getPluginInfos(roles,getLanguage()).then(response => {
          let plugin_infos = response.data
          plugin_infos.forEach(plugin_info => {
            let pluginChildren = [
              {
                path: 'dashboard',
                component: () => import('@/views/plugin/dashboard/dashboard'),
                name: 'pluginDashboard_' + plugin_info.name,
                meta: {title: 'dashboard'}
              },
              {
                path: 'setting',
                component: () => import('@/views/plugin/setting/setting'),
                name: 'pluginSetting_' + plugin_info.name,
                meta: {title: 'pluginSetting'}
              },
              {
                path: plugin_info.github,
                component: Layout,
                name: 'pluginGitHub_' + plugin_info.name,
                meta: {title: 'github'}
              },
            ]

            if (roles.includes('admin')) {
              pluginChildren.push({
                  path: 'log',
                  component: () => import('@/views/plugin/log/log'),
                  name: 'pluginLog_' + plugin_info.name,
                  meta: {title: 'log'}
                }
              )
            }
            pluginRoutes.push(
              {
                path: plugin_info.name + '/',
                name: plugin_info.name,
                component: () => import('@/views/plugin/index'),
                meta: {
                  title: plugin_info.tittle,
                  icon: 'nested'
                },
                children: pluginChildren
              }
            )
          })
          accessedRoutes.push({
            path: '/plugin/',
            component: Layout,
            name: 'plugin',
            meta: {
              title: 'plugin',
              icon: 'component'
            },
            children: pluginRoutes
          })
          if (roles.includes('admin')) {
            accessedRoutes = accessedRoutes.concat(getAdminRouter())
          }
          // 404 page must be placed at the end !!!
          accessedRoutes.push({ path: '*', redirect: '/404', hidden: true })
          commit('SET_ROUTES', accessedRoutes)
          resolve(accessedRoutes)
        }
      )
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
