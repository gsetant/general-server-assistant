import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/401'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: {title: 'dashboard', icon: 'dashboard'}
    }]
  },
  {
    path: '/manualSearch',
    component: Layout,
    redirect: '/manualSearch',
    children: [{
      path: 'manualSearch',
      name: 'manualSearch',
      component: () => import('@/views/manualSearch/index'),
      meta: {title: 'manualSearch', icon: 'form'}
    }]
  },
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    hidden: true,
    children: [
      {
        path: 'index',
        component: () => import('@/views/profile/index'),
        name: 'Profile',
        meta: {title: 'profile', icon: 'user', noCache: true}
      }
    ]
  },
  {
    path: '/library',
    component: Layout,
    redirect: '/library/config',
    children: [
      {
        path: 'config',
        component: () => import('@/views/libraryConfig/index'),
        name: 'libraryConfig',
        meta: {title: 'library', icon: 'list', noCache: true}
      },
      {
        path: 'edit',
        component: () => import('@/views/libraryConfig/edit/edit'),
        name: 'libraryEdit',
        meta: {title: 'library', icon: 'list', noCache: true},
        hidden: true,
      },
    ]
  }
]

/**
 * adminRoutes
 * the routes that only admin could access
 */
export const adminRoutes = [
  {
    path: '/admin/',
    component: Layout,
    meta: {
      title: 'adminPages',
      icon: 'user'
    },
    children: [
      {
        path: 'admin/log',
        name: 'adminLog',
        component: () => import('@/views/admin/adminLog'),
        meta: {
          title: 'adminLog',
        },
      },
      {
        path: 'plugin/management',
        name: 'pluginManagement',
        component: () => import('@/views/admin/plugManagement'),
        meta: {
          title: 'pluginManagement',
        },
      },
      {
        path: 'user/management',
        name: 'pluginManagement',
        component: () => import('@/views/admin/userManagement'),
        meta: {
          title: 'userManagement',
        },
      }]
  }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({y: 0}),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
