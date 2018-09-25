<template>
  <v-container fluid grid-list-sm>
      <v-slide-y-transition>
      <v-layout row wrap>
          <template v-for="post in postTree">
              <Post class="xs8 md6" :post="post" :key="post.id"/>
          </template>
      </v-layout>
      </v-slide-y-transition>
  </v-container>
</template>

<script>
import Post from '../components/Post.vue';
import POSTS from '../graphql/Posts.gql'
import _ from 'lodash'

export default {
  props: {
      location: !String
  },
  components: {
      Post,
  },
  apollo: {
    allPosts: {
      query: POSTS,
      variables() {
        return {
          location: this.location
        }
      }
    }
  },
  data() {
    return {
        isLoading: true,
        posts: null,
    }
  },
  computed: {
    postTree() {
      if (!this.allPosts) return []
      return _.map(this.allPosts.edges, e => e.node)

      let edges = _.cloneDeep(this.allPosts.edges)
      let lookup = _.keyBy(edges, e => e.node.address)
      let roots = []
      let topic_end = this.$props.location.indexOf('/')
      topic_end += 1
      let depth = Math.floor((this.$props.location.length - topic_end) / 44)
      if (depth < 1) depth = 1;
      _.map(edges, function (edge) {
          let post = edge.node
          if (post.chainLevel > depth) {
              let parent = lookup[post.to]
              if (parent) {
                  parent = parent.node //TODO do this during keyBy
                  if (!parent.children) {
                      parent.children = []
                  }
                  parent.children.push(post)
              }
          } else {
              roots.push(post)
          }
      })
      console.log(results, roots, lookup)
      return roots
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
