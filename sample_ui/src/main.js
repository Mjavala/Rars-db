import Vue from "vue";
import App from "./App.vue";
import VueApollo from 'vue-apollo'
import ApolloClient from "apollo-client";
import { WebSocketLink } from 'apollo-link-ws';
import { InMemoryCache } from "apollo-cache-inmemory";

Vue.use(VueApollo);
Vue.config.productionTip = false;

const getHeaders = () => {
  const headers = {
    'content-type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'x-hasura-access-key': 'myadminsecretkey'
  }

  return headers;
};

// Create a WebSocket link:

const link = new WebSocketLink({

 uri: 'ws://localhost:8080/v1/graphql',

 options: {

   reconnect: true,

   timeout: 30000,

   connectionParams: () => {

     return { headers: getHeaders() };

   },
 }
});
const client = new ApolloClient({
  link: link,
  cache: new InMemoryCache({
    addTypename: true
  })
});
const apolloProvider = new VueApollo({
  defaultClient: client,
})
new Vue({
  apolloProvider,
  render: h => h(App)
}).$mount("#app");