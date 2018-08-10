<template>
  <div>
  <div class="location">
      <v-input v-model="location" label="Location"/>
  </div>
  <div class="new-post">
  <router-link :to="`/reply/${location}`" class="post-reply">
    <v-btn>Post</v-btn>
  </router-link>
  </div>
  <div class="posts">
      <ApolloQuery
        :query="require('../graphql/Posts.gql')"
        :variables="{location}"
      >
        <div slot-scope="{ result: { data } }">
          <template v-if="data">
            <div
              v-for="post of data.allPosts.edges"
              :key="post.id"
              class="post"
            >
                <div class="post-to">{{post.to}}</div>
                <div class="post-signer">{{post.signer}}</div>
                <div class="post-link">{{post.link}}</div>
                <router-link :to="`/reply/${post.to}`" class="post-reply">
                  <v-btn>Reply</v-btn>
                </router-link>
            </div>
          </template>
        </div>
      </ApolloQuery>
  </div>
  </div>
</template>

<script>

export default {
  name: 'Posts',
  data () {
    return {
        location: ''
    }
  },
  computed: {
  },

  methods: {
  },
}
</script>

<style scoped>

</style>
