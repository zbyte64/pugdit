<template>
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
</template>

<script>
import {getGraphId} from '../mailbox.js'
import VOTE from '../graphql/Vote.gql'
import _ from 'lodash'

export default {
  name: 'Score',
  props: {
    post: !Object
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
  },
}
</script>

<style scoped>

</style>
