<template>
    <ApolloQuery
      :query="require('../graphql/AuthSelf.gql')"
    >
      <div slot-scope="{ result: { data } }">
        <template v-if="data && data.authUser">
            <div>hello {{data.authUser.email}}</div>
        </template>
        <template v-else>
            <v-btn href="/accounts/signup/">Sign In</v-btn>
        </template>
      </div>
    </ApolloQuery>
</template>

<script>
export default {
  name: 'AuthStatus',
}
</script>

<style>
</style>
