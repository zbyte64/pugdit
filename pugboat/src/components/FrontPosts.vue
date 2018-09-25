<template>
  <v-layout column>
  <v-flex>
      <v-text-field v-model="location" label="Location"/>
  </v-flex>
  <div v-if="authUser">
      <v-flex class="new-post" v-if="location">
          <router-link :to="`/reply/${location}`">
            <v-btn>Post</v-btn>
          </router-link>
      </v-flex>
  </div>
  <v-flex>
    <v-layout v-if="posts">
      <Post :post="post" v-for="post in posts" @click="viewPost(post)" :key="post.id"/>
    </v-layout>
  </v-flex>
  </v-layout>
</template>

<script>
import Post from './Post.vue'
import AUTH_SELF from '../graphql/AuthSelf.gql'
import FRONT_POSTS from '../graphql/FrontPosts.gql'

export default {
  name: 'FrontPosts',
  components: {
    Post,
  },
  apollo: {
    authUser: AUTH_SELF,
    allPosts: {
      query: FRONT_POSTS,
      variables() {
        return {
          location: this.location
        }
      }
    }
  },
  data () {
    return {
        location: ''
    }
  },
  computed: {
      posts() {
          if (!this.allPosts) return []
          return this.allPosts.edges.map(x => x.node)
      }
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
