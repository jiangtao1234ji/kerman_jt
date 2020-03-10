import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '../layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
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
    component: () => import('../views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('../views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('../views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('../views/error-page/401'),
    hidden: true
  },
  {
    path: '',
    component: Layout,
    redirect: '/blog',
    hidden: false
  }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  {
    path: '/blog',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('../views/blog/list'),
        name: 'Blogs',
        meta: { title: 'blogs', icon: 'list' }
      },
      {
        path: 'create',
        component: () => import('../views/blog/create'),
        name: 'CreateBlog',
        meta: { title: 'createBlog', icon: 'edit' },
        hidden: true
      },
      {
        path: 'edit/:id(\\d+)',
        component: () => import('../views/blog/edit'),
        name: 'EditBlog',
        meta: { title: 'editBlog', noCache: true, activeMenu: '/blog/list' },
        hidden: true
      }
    ]
  },
  {
    path: '/page',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('../views/page/list'),
        name: 'Pages',
        meta: { title: 'pages', icon: 'documentation' }
      },
      {
        path: 'create',
        component: () => import('../views/page/create'),
        name: 'CreatePage',
        meta: { title: 'createPage', icon: 'edit' },
        hidden: true
      },
      {
        path: 'edit/:id(\\d+)',
        component: () => import('../views/page/edit'),
        name: 'EditPage',
        meta: { title: 'editPage', noCache: true, activeMenu: '/page/list' },
        hidden: true
      }
    ]
  },
  {
    path: '/settings',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('../views/settings'),
        name: 'Settings',
        meta: { title: 'settings', icon: 'settings' }
      }
    ]
  },
  // {
  //   path: '/comment',
  //   component: Layout,
  //   children: [
  //     {
  //       path: '',
  //       component: () => import('../views/comment/list'),
  //       name: 'Comments',
  //       meta: {title: 'comments', icon: 'comment'}
  //     }
  //   ]
  // },

  {
    path: '/integration',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('../views/integration'),
        name: 'Integration',
        meta: { title: 'integration', icon: 'example' }
      }
    ]
  },
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () =>
  new Router({
    // mode: 'history', // require service support
    scrollBehavior: () => ({ y: 0 }),
    routes: constantRoutes
  })

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
