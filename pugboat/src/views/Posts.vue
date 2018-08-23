<template>
  <v-container fluid grid-list-sm>
      <v-layout row wrap>
          <template v-for="post in posts" v-if="!isLoading">
              <Post :post="post" :key="post.id" />
          </template>
      </v-layout>
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
    data() {
      return {
          isLoading: true,
          posts: null
      }
    },
    created() {
        this.postTree().then(roots => {
            this.posts = roots
            this.isLoading = false
        })
    },
    methods: {
        async postTree() {
          let results = await this.$apollo.query({
            query: POSTS,
            variables: {
                location: this.$props.location,
            }
          })
          let edges = _.cloneDeep(results.data.allPosts.edges)
          let lookup = _.keyBy(edges, e => e.node.address)
          let roots = []
          let topic_end = this.$props.location.indexOf('/')
          topic_end += 1
          let depth = Math.floor((this.$props.location.length - topic_end) / 44)
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
    },
    watch: {
        location: function() {
            this.isLoading = true
            this.postTree().then(roots => {
                this.posts = roots
                this.isLoading = false
            })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
