<template>
  <div class="post-mark">
    <wysiwyg v-model="newMessage" />
    <v-btn
      @click="formValid && uploadMessage()"
    >Upload</v-btn>
  </div>
</template>

<script>
import POST_MARK from '../graphql/PostMark.gql'
import AUTH_SELF from '../graphql/AuthSelf.gql'
import {sign, decodeBase64} from '../mailbox.js'
import msgpack from 'msgpack-lite'


export default {
  props: {
    to: !String
  },
  data () {
    return {
      newMessage: '',
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
      let payload = msgpack.encode([this.$props.to, link])
      let v = msgpack.decode(payload)
      console.log(v)
      console.log(payload)
      let signature = sign(payload)
      let signer = Buffer.from(await this.getSigner(), 'base64').toString('ascii').split(':')[1];
      let result = await this.$apollo.mutate({
        mutation: POST_MARK,
        variables: {
            //to: this.$props.to,
            signer: signer,
            //link: link,
            signature: signature,
        }
      })
      this.$data.link = link
      this.$data.signature = signature
      console.log(result)
      let address = result.data.postMark.post.address
      this.$router.push({ path: `/p/${address}`})
    },
    async getSigner() {
      //TODO dont assume its the first identity signing
      let r = await this.$apollo.query({
        query: AUTH_SELF,
      })
      console.log(r)
      return r.data.authUser.identitySet.edges[0].node.id
    }
  }
}
</script>

<style scoped>
@import "~vue-wysiwyg/dist/vueWysiwyg.css";
</style>
