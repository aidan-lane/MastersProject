import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false;

const axios = require("axios").default;
axios.defaults.baseURL = "http://localhost:5000";
Vue.prototype.$http = axios;

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
