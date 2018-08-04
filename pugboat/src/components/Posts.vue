<template>
  <div>
  <div class="location">
      <input v-model="location"/>
  </div>
  <div class="posts">
      <ApolloQuery
        :query="require('../graphql/Posts.gql')"
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
                  <div color="navy" class="button">
                    <p class="big-text">Reply</p>
                  </div>
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
  computed:
  },

  methods: {
  },
}
</script>

<style scoped>

</style>
