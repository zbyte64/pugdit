import '@babel/polyfill'
import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import { createProvider } from './vue-apollo'
import router from './router'
import store from './store'

Vue.config.productionTip = false

new Vue({
  provide: createProvider().provide(),
  router,
  store,
  render: h => h(App)
}).$mount('#app')
