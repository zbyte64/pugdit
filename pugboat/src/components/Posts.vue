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

export default {
  name: 'Posts',
  props: {
    location: !String
  },
  computed: {
  },

  methods: {
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
