<template>
  <div>
  <div class="location">
      <v-input v-model="location" label="Location"/>
  </div>
  <div class="new-post" v-if="location">
  <router-link :to="`/reply/${location}`" class="post-reply">
    <v-btn>Post</v-btn>
  </router-link>
  </div>
  <div class="posts">
      <ApolloQuery
        :query="require('../graphql/FrontPosts.gql')"
        :variables="{location}"
      >
        <div slot-scope="{ result: { data } }">
          <template v-if="data">
            <v-list>
            <v-list-tile
              v-for="e of data.allPosts.edges"
              :key="e.node.id"
              class="post"
              @click="viewPost(e.node)"
            >
                <!--div class="post-to">{{e.node.to}}</div-->
                <v-list-tile-avatar class="post-signer">
                    <v-gravatar :hash="e.node.signer.public_key" />
                </v-list-tile-avatar>
                <!--div class="post-link">{{e.node.link}}</div-->
                <v-list-tile-content v-if="e.node.file">
                    <div class="post-content">{{e.node.file.content|sanitize}}</div>
                </v-list-tile-content>
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
  name: 'FrontPosts',
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
