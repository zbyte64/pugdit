<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
          <h2>Profile</h2>
          <div>
          <ApolloQuery
            :query="require('../graphql/AuthSelf.gql')"
            @result="readUser"
          >
            <div slot-scope="{ result: { data } }">
              <template v-if="data && data.authUser">
                  <div><label>username:</label> {{data.authUser.username}}</div>
                  <div><label>email:</label> {{data.authUser.email}}</div>
                <div
                  v-for="identity of data.authUser.identitySet.edges"
                  :key="identity.id"
                  class="identity"
                >
                    <div class="public_key">{{identity.public_key}}</div>
                </div>
              <button v-if="!data.authUser.identitySet.edges || !key" @click="registerIdentity">Register Identity</button>
              </template>
              <template v-else>
                  <ApolloMutation
                    :mutation="require('../graphql/Login.gql')"
                    :variables="{
                      username: username,
                      password: password
                    }"
                    class="form"
                  >
                    <template slot-scope="{ mutate }">
                        <input
                          v-model="username"
                          placeholder="Type your username"
                          class="input"
                          type="text"
                        >
                      <input
                        v-model="password"
                        placeholder="Type your password"
                        class="input"
                        type="password"
                        @keyup.enter="mutate()"
                      >
                    </template>
                  </ApolloMutation>
              </template>
            </div>
          </ApolloQuery>

      </div>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
import REGISTER_IDENTITY from '../graphql/RegisterIdentity.gql'
import {newIdentity, loadKey} from '../mailbox.js';

export default {
    data() {
        return {
            key: loadKey(),
            username: '',
            password: ''
        }
    },
    methods: {
        readUser(result) {
            if (!result.data) return
            let user = result.data.authUser
            if (!user) return
            this.$data.username = user.username
        },
        async registerIdentity () {
          let {public_key, signed_username} = newIdentity(this.$data.username);
          await this.$apollo.mutate({
            mutation: REGISTER_IDENTITY,
            variables: {
                signed_username: signed_username,
                public_key: public_key,
            }
          })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
