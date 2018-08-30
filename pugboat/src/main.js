import '@babel/polyfill';
import Vue from 'vue';
import './plugins/vuetify';
import App from './App.vue';
import { createProvider } from './vue-apollo';
import router from './router';
import store from './store';
import wysiwyg from "vue-wysiwyg";
import VueResource from 'vue-resource';
import Cookies from 'js-cookie';
import Gravatar from 'vue-gravatar';
import './registerServiceWorker'

Vue.use(VueResource);
Vue.component('v-gravatar', Gravatar);

const csrftoken = Cookies.get('csrftoken');
Vue.http.headers.common['X_CSRFTOKEN'] = csrftoken;

Vue.use(wysiwyg, {
  image: {
    uploadURL: "/api/add-asset/",
    dropzoneOptions: {
      url: "/api/add-asset/",
      headers: { "X-CSRFTOKEN": csrftoken }
    }
  },
});

Vue.config.productionTip = false;

new Vue({
  provide: createProvider().provide(),
  router,
  store,
  render: h => h(App)
}).$mount('#app');
