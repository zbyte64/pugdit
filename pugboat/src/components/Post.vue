<template>
    <div>
    <v-card :href="`/p/${this.post.address}`">
      <template v-if="post.file">
          <v-card-media v-if="isImage" :src="`data:${post.file.contentType};base64, ${post.file.content}`" height="300px"/>
          <v-card-text v-else v-html="this.sanitize(post.file.content)"/>
      </template>
      <!--div class="post-to">{{post.to}}</div-->
      <v-card-title primary-title class="post-signer">
          <v-gravatar :hash="post.signer.publicKey" />
          <v-subheader>Karma: {{post.karma}}</v-subheader>
      </v-card-title>
      <!--div class="post-link">{{post.link}}</div-->
      <v-card-actions>
          <v-btn flat icon color="blue lighten-2" @click="vote(1)">
            <v-icon>thumb_up</v-icon>
          </v-btn>
          <v-btn flat icon color="red lighten-2" @click="vote(-1)">
            <v-icon>thumb_down</v-icon>
          </v-btn>
          <router-link :to="`/reply/${post.address}`" class="post-reply">
            <v-btn>Reply</v-btn>
          </router-link>
      </v-card-actions>
  </v-card>
  <template v-for="replyPost in post.children">
      <Post :post="replyPost" :key="replyPost.id" />
  </template>
  </div>
</template>

<script>
import sanitizeHtml from 'sanitize-html';
import VOTE from '../graphql/Vote.gql'
import _ from 'lodash'

export default {
  name: 'Post',
  props: {
    post: !Object
  },
  computed: {
    isImage() {
        return _.startsWith(this.post.file.contentType, 'image')
    }
  },
  methods: {
      async vote(karma) {
          await this.$apollo.mutate({
            mutation: VOTE,
            variables: {
                post: this.post.id,
                karma,
            }
          })
      },
      viewPost() {
          this.$router.push({ path: `/p/${this.post.address}`})
      },
      sanitize: function (value) {
        if (!value) return ''
        value = value.toString()
        return sanitizeHtml(value, {
          allowedTags: sanitizeHtml.defaults.allowedTags.concat([ 'img' ])
        })
      },
  },
}
</script>

<style scoped>

</style>
