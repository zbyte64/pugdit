<template>
  <div v-if="!isLoading">
    <template v-if="user">
        <div>hello {{user.email}}</div>
    </template>
    <template v-else>
        <v-btn href="/accounts/signup/">Sign In</v-btn>
    </template>
  </div>
</template>

<script>
import AUTH_USER from '../graphql/AuthSelf.gql';
import {setLockerAuth, LOCKER} from '../mailbox.js';

export default {
  name: 'AuthStatus',
  data() {
      return {
          isLoading: true,
          user: null
      }
  },
  created() {
      this.loadUser()
  },
  methods: {
      loadUser() {
          return this.$apollo.query({
              query: AUTH_USER
          }).then(response => {
              let user = response.data.authUser;
              this.$data.user = user;
              this.$data.isLoading = false;
              if (user) {
                  setLockerAuth(user.username, user.storageKey)
              }
          }).catch(error => {
              this.error = error
              console.log(error)
          })
      }
  }
}
</script>

<style>
</style>
