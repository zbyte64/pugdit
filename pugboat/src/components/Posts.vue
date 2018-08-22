<template>
  <div>
  <template v-for="post in posts" v-if="!isLoading">
      <Post :post="post" :key="post.id" />
  </template>
  </div>
</template>

<script>
import POSTS from '../graphql/Posts.gql'
import Post from './Post.vue'
import _ from 'lodash'

export default {
  name: 'Posts',
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
        let depth =  (this.$props.location.match(/\//g)||[]).length
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

<style scoped>

</style>
