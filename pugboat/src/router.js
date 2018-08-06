import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Reply from './views/Reply.vue';
import Profile from './views/Profile.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
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
