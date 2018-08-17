<template>
    <div>
    <v-list-tile>
      <v-list-tile-action >
          <v-btn flat icon color="blue lighten-2" @click="vote(1)">
            <v-icon>thumb_up</v-icon>
          </v-btn>
          <v-subheader>{{post.karma}}</v-subheader>
          <v-btn flat icon color="red lighten-2" @click="vote(-1)">
            <v-icon>thumb_down</v-icon>
          </v-btn>
      </v-list-tile-action>
      <!--div class="post-to">{{post.to}}</div-->
      <v-list-tile-avatar class="post-signer">
          <v-gravatar :hash="post.signer.publicKey" />
      </v-list-tile-avatar>
      <!--div class="post-link">{{post.link}}</div-->
      <v-list-tile-content v-if="post.file">
          <div class="post-content" v-html="this.sanitize(post.file.content)"></div>
      </v-list-tile-content>
      <v-list-tile-action>
          <router-link :to="`/reply/${post.address}`" class="post-reply">
            <v-btn>Reply</v-btn>
          </router-link>
      </v-list-tile-action>
  </v-list-tile>
  <template v-for="replyPost in post.children">
      <Post :post="replyPost" :key="replyPost.id" />
  </template>
  </div>
</template>

<script>
import sanitizeHtml from 'sanitize-html';
import VOTE from '../graphql/Vote.gql'

export default {
  name: 'Post',
  props: {
    post: !Object
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
