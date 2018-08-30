<template>
  <v-layout column>
  <v-flex>
      <v-text-field v-model="location" label="Location"/>
  </v-flex>
  <ApolloQuery
    :query="require('../graphql/AuthSelf.gql')"
  >
    <div slot-scope="{ result: { data } }">
      <template v-if="data && data.authUser">
          <v-flex class="new-post" v-if="location">
              <router-link :to="`/reply/${location}`">
                <v-btn>Post</v-btn>
              </router-link>
          </v-flex>
      </template>
    </div>
  </ApolloQuery>
  <v-flex>
  <ApolloQuery
    :query="require('../graphql/FrontPosts.gql')"
    :variables="{location}"
  >
    <v-layout slot-scope="{ result: { data } }" v-if="data">
      <Post :post="e.node" v-for="e of data.allPosts.edges" @click="viewPost(e.node)" :key="e.node.id"/>
  </v-layout>
  </ApolloQuery>
  </v-flex>
  </v-layout>
</template>

<script>
import Post from './Post.vue'

export default {
  name: 'FrontPosts',
  components: {
      Post,
  },
  data () {
    return {
        location: ''
    }
  },
  computed: {
  },
  methods: {
      viewPost(post) {
          this.$router.push({ path: `/p/${post.address}`})
      }
  }
}
</script>

<style scoped>

</style>
