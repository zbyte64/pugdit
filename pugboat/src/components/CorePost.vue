<template>
    <v-card :to="`/p/${this.post.address}`" flat tile>
      <template v-if="post.file">
          <v-card-media contain v-if="isImage" :src="post.link" height="150px"/>
          <v-card-text v-else v-html="this.sanitize(post.file.content)"/>
      </template>
      <!--div class="post-to">{{post.to}}</div-->
      <v-card-title>
          <avatar :user="post.signer" />
          <v-subheader>Karma: {{post.karma}}</v-subheader>
      </v-card-title>
      <!--div class="post-link">{{post.link}}</div-->
      <v-card-actions>
          <v-btn flat icon color="blue lighten-2" @click.prevent="vote(1)">
            <v-icon>thumb_up</v-icon>
          </v-btn>
          <v-btn flat icon color="red lighten-2" @click.prevent="vote(-1)">
            <v-icon>thumb_down</v-icon>
          </v-btn>
          <v-btn flat icon color="grey" :to="`/reply/${post.address}`">
            Reply
          </v-btn>
      </v-card-actions>
  </v-card>
</template>

<script>
import Avatar from './Avatar.vue'
import sanitizeHtml from 'sanitize-html';
import {getGraphId} from '../mailbox.js'
import VOTE from '../graphql/Vote.gql'
import _ from 'lodash'

export default {
  name: 'CorePost',
  props: {
    post: !Object
  },
  components: {
    Avatar
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
                post: getGraphId(this.post.id),
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
          //allowedTags: sanitizeHtml.defaults.allowedTags.concat([ 'img' ])
        })
      },
  },
}
</script>

<style scoped>

</style>
