<template>
  <div>
  <div class="posts">
      <ApolloQuery
        :query="require('../graphql/Posts.gql')"
        :variables="{location}"
      >
        <div slot-scope="{ result: { data } }">
          <template v-if="data">
              <v-list>
              <v-list-tile
                v-for="e of data.allPosts.edges"
                :key="e.node.id"
                class="post"
              >
                  <v-list-tile-action >
                      <v-btn flat icon color="blue lighten-2" @click="voteUp(e.node)">
                        <v-icon>thumb_up</v-icon>
                      </v-btn>
                      <v-subheader>{{e.node.karma}}</v-subheader>
                      <v-btn flat icon color="red lighten-2" @click="voteDown(e.node)">
                        <v-icon>thumb_down</v-icon>
                      </v-btn>
                  </v-list-tile-action>
                  <!--div class="post-to">{{e.node.to}}</div-->
                  <v-list-tile-avatar class="post-signer">
                      <v-gravatar :hash="e.node.signer.public_key" />
                  </v-list-tile-avatar>
                  <!--div class="post-link">{{e.node.link}}</div-->
                  <v-list-tile-content v-if="e.node.file">
                      <div class="post-content">{{e.node.file.content|sanitize}}</div>
                  </v-list-tile-content>
                  <v-list-tile-action>
                      <router-link :to="`/reply/${e.node.address}`" class="post-reply">
                        <v-btn>Reply</v-btn>
                      </router-link>
                  </v-list-tile-action>
              </v-list-tile>
              </v-list>
          </template>
        </div>
      </ApolloQuery>
  </div>
  </div>
</template>

<script>
import sanitizeHtml from 'sanitize-html';
import VOTE from '../graphql/Vote.gql'

export default {
  name: 'Posts',
  props: {
    location: !String
  },
  computed: {
  },

  methods: {
      async vote(post, karma) {
          await this.$apollo.mutate({
            mutation: VOTE,
            variables: {
                post: post.id,
                karma,
            }
          })
      },
      async voteUp(post) {
          await this.vote(post, 1)
      },
      async voteDown(post) {
          await this.vote(post, -1)
      },
  },
  filters: {
    sanitize: function (value) {
      if (!value) return ''
      value = value.toString()
      return sanitizeHtml(value)
    }
  }
}
</script>

<style scoped>

</style>
