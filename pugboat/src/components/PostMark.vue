<template>
  <div class="post-mark">
    <wysiwyg v-model="newMessage" />
    <button
      @click="formValid && uploadMessage()"
    >Upload</button>
  </div>
</template>

<script>
import POST_MARK from '../graphql/PostMark.gql'
import {sign} from '../mailbox.js'

export default {
  props: {
    to: !String
  },
  data () {
    return {
      newMessage: '',
      timestamp: '',
      signer: 1,
      link: '',
      signature: '',
    }
  },

  apollo: {
    postMark: POST_MARK,
  },

  computed: {
    formValid () {
      return this.newMessage
    }
  },

  methods: {
    async uploadMessage () {
      if (!this.formValid) return
      //TODO indicate mimetype
      let response = await this.$http.post('/api/add-asset/', {filename: 'post', content:this.$data.newMessage})
      let link = response.data
      let payload = [this.$props.to, link, this.$data.timestamp].join(',')
      let signature = sign(payload)
      await this.$apollo.mutate({
        mutation: POST_MARK,
        variables: {
            to: this.$props.to,
            timestamp: this.$data.timestamp,
            signer: this.$data.signer,
            link: link,
            signature: signature,
        }
      })
    }
  },
}
</script>

<style scoped>
@import "~vue-wysiwyg/dist/vueWysiwyg.css";

.form,
.input,
.apollo,
.message {
  padding: 12px;
}

.input {
  font-family: inherit;
  font-size: inherit;
  border: solid 2px #ccc;
  border-radius: 3px;
}

.error {
  color: red;
}

.images {
  display: grid;
  grid-template-columns: repeat(auto-fill, 300px);
  grid-auto-rows: 300px;
  grid-gap: 10px;
}

.image-item {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ccc;
  border-radius: 8px;
}

.image {
  max-width: 100%;
  max-height: 100%;
}

.image-input {
  margin: 20px;
}
</style>
