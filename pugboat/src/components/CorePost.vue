<template>
    <v-card :to="`/p/${this.post.address}`" flat tile>
      <template v-if="post.file">
          <a v-if="isImage" :href="post.link" target="_blank">
            <v-card-media contain :src="post.link" :height="activeImgHeight"/>
          </a>
          <v-card-text v-else v-html="this.sanitize(post.file.content)"/>
      </template>
      <v-card-title>
        <div>
          <v-btn small flat v-if="post.chainLevel == 0" :to="`/p/${this.post.to}`">
            [ {{post.to}} ]
          </v-btn>
          <v-btn small flat v-else :to="`/p/${this.post.to}`">
            [ parent ]
          </v-btn>
          <div v-if="post.responseCount">{{post.responseCount}} comments</div>
          <div>received {{postedAt}}</div>
        </div>
      </v-card-title>
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
          <ApolloQuery
            :query="require('../graphql/AuthSelf.gql')"
          >
            <div slot-scope="{ result: { data } }">
              <template v-if="data && data.authUser">
                  <v-btn icon color="grey" :to="`/reply/${post.address}`">
                    <v-icon>reply</v-icon>
                  </v-btn>
              </template>
            </div>
          </ApolloQuery>
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
import moment from 'moment'

export default {
  name: 'CorePost',
  props: {
    post: !Object
  },
  components: {
    Avatar
  },
  data() {
    return {
        activeImgHeight: 150,
    }
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
    postedAt() {
        return moment(this.$props.post.receivedTimestamp).fromNow()
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
