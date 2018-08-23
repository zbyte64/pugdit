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
                  v-for="node of data.authUser.identities"
                  :key="node.id"
                  class="identity"
                >
                    <div class="publicKey"><label>public key:</label>{{node.publicKey}}</div>
                </div>
              <v-btn v-if="!data.authUser.identities.length || !key" @click="registerIdentity">Register Identity</v-btn>
              </template>
              <template v-else>
                  <v-alert type="error" :value="error&&1">{{error}}</v-alert>
                  <v-form v-on:submit.prevent="login">
                    <v-text-field
                      v-model="username"
                      label="Username"
                      placeholder="Type your username"
                    />
                      <v-text-field
                        v-model="password"
                        label="Password"
                        placeholder="Type your password"
                        type="password"
                      />
                      <v-btn @click="login">Login</v-btn>
                  </v-form>
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
import LOGIN from '../graphql/Login.gql'
import {newIdentity, loadKey} from '../mailbox.js';

export default {
    data() {
        return {
            key: loadKey(),
            username: '',
            password: '',
            error: null
        }
    },
    methods: {
        readUser(result) {
            if (!result.data) return
            let user = result.data.authUser
            if (!user) return
            this.$data.username = user.username
        },
        async login() {
          this.error = null
          await this.$apollo.mutate({
              mutation: LOGIN,
              variables: {
                  username: this.$data.username,
                  password: this.$data.password,
              }
          }).then(() => {
              this.$router.push({ path: `/profile`})
          }).catch(error => {
              this.error = error
              console.log(error)
          })
        },
        async registerIdentity () {
          let {public_key, signed_username} = newIdentity(this.$data.username);
          console.log('su', signed_username)
          this.$data.key = public_key
          await this.$apollo.mutate({
            mutation: REGISTER_IDENTITY,
            variables: {
                signedUsername: signed_username,
                publicKey: public_key,
            }
          })
          this.$router.push({ path: `/profile`})
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
