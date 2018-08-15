import Vue from 'vue';
import Router from 'vue-router';
import Reply from './views/Reply.vue';
import Profile from './views/Profile.vue';
import Posts from './views/Posts.vue';
import FrontPage from './views/FrontPage.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'frontpage',
      component: FrontPage
    },
    {
      path: '/p/*',
      name: 'posts',
      component: Posts,
      props: (route) => ({location: route.path.substr(3)})
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile
    },
    {
      path: '/reply/*',
      name: 'reply',
      component: Reply,
      props: (route) => ({to: route.path.substr(7)})
    }
  ],
});
