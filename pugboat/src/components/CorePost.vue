<template>
    <v-card :to="`/p/${this.post.address}`" flat tile>
      <template v-if="post.file">
          <v-card-media contain v-if="isImage" :src="post.link" height="150px"/>
          <v-card-text v-else v-html="this.sanitize(post.file.content)"/>
      </template>
      <!--div class="post-to">{{post.to}}</div-->
      <v-card-actions>
          <v-avatar>
              <avatar :user="post.signer" />
          </v-avatar>
          <v-spacer/>
          <v-btn icon :disabled="downVoted" color="red lighten-2" @click.prevent="vote(-1)">
            <v-icon>thumb_down</v-icon>
          </v-btn>
          <v-subheader color="grey">
              {{post.karma}}
          </v-subheader>
            <v-btn icon :disabled="upVoted" color="blue lighten-2" @click.prevent="vote(1)">
              <v-icon>thumb_up</v-icon>
            </v-btn>
          <v-spacer/>
          <v-btn icon color="grey" :to="`/reply/${post.address}`">
            <v-icon>reply</v-icon>
          </v-btn>
      </v-card-actions>
  </v-card>
</template>

<script>
import Avatar from './Avatar.vue'
import sanitizeHtml from 'sanitize-html';
import {getGraphId} from '../mailbox.js'
import VOTE from '../graphql/Vote.gql'
import POST from '../graphql/PostFragment.gql'
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
    },
    downVoted() {
        let vote = this.$props.post.userVote
        if (!vote) return false
        return vote.karma == -1
    },
    upVoted() {
        let vote = this.$props.post.userVote
        if (!vote) return false
        return vote.karma == 1
    },
  },
  methods: {
      async vote(karma) {
          let response = await this.$apollo.mutate({
            mutation: VOTE,
            variables: {
                post: getGraphId(this.post.id),
                karma,
            }
          })
          console.log('vote response', response)
          let vote = response.data.vote.vote
          let voteUpdate = {
              userVote: vote
          }
          this.$apollo.getClient().writeFragment({
              //id: this.post.id,
              fragment: POST,
              data: _.assign({}, this.post, vote.post, voteUpdate)
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
