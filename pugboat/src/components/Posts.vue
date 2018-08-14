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
              v-for="e of data.allPosts.edges"
              :key="e.node.id"
              class="post"
            >
                <div class="post-to">{{e.node.to}}</div>
                <div class="post-signer">{{e.node.signer.id}}</div>
                <div class="post-link">{{e.node.link}}</div>
                <div v-if="e.node.file">
                    <div class="post-content-type">{{e.node.file.contentType}}</div>
                    <div class="post-content">{{e.node.file.content|sanitize}}</div>
                </div>
                <router-link :to="`/reply/${e.node.to}`" class="post-reply">
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
import sanitizeHtml from 'sanitize-html';

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
