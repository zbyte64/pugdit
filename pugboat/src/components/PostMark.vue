<template>
  <div class="post-mark">
    <v-alert type="error" :value="error&&1">{{error}}</v-alert>
    <v-radio-group v-model="postType">
      <v-radio label="Compose" value="newPost"/>
      <v-radio label="Link" value="link"/>
    </v-radio-group>
    <v-text-field v-model="subject" label="Subject"/>
    <div v-if="postType == 'newPost'">
        <v-label>Optional Image</v-label>
        <div v-if="imageLink">currently: {{imageLink}}</div>
        <upload-btn accept="image/png, image/jpeg, image/gif"
            :fileChangedCallback="uploadImage"></upload-btn>
        <wysiwyg v-model="newMessage"/>
    </div>
    <div v-if="postType == 'link'">
        <v-text-field v-model="link" label="URL link"/>
    </div>
    <v-btn :active="formValid"
      @click="formValid && submit()"
    >Upload</v-btn>
  </div>
</template>

<script>
import POST_MARK from '../graphql/PostMark.gql'
import AUTH_SELF from '../graphql/AuthSelf.gql'
import REGISTER_IDENTITY from '../graphql/RegisterIdentity.gql'
import {sign, getGraphId, LOCKER, buildRFC822} from '../mailbox.js'
import UploadButton from 'vuetify-upload-button';
import msgpack from 'msgpack-lite'
import _ from 'lodash'


export default {
  props: {
    to: !String
  },
  components: {
    'upload-btn': UploadButton
  },
  data () {
    return {
      postType: 'newPost',
      subject: '',
      newMessage: '',
      imageLink: null,
      link: '',
      signature: '',
      error: null,
    }
  },
  computed: {
    formValid () {
      switch(this.$data.postType) {
        case 'newPost':
          return this.newMessage && this.subject
        case 'link':
          return this.link
      }
      return false
    }
  },
  methods: {
    async submit() {
        this.error = null
        await this._submit()/*.catch(error => {
            this.error = error
        })*/
    },
    async _submit() {
        switch(this.$data.postType) {
          case 'newPost':
            return await this.uploadMessage()
          case 'link':
            return await this.postMarkLink(this.link)
        }
    },
    async uploadImage(e) {
        console.log("upload", e)
        var formData = new FormData();
        formData.append('file', e);
        let response = await this.$http.post('/api/add-asset/', formData)
        this.imageLink = response.data
    },
    async uploadMessage () {
      if (!this.formValid) return
      let headers = [
          ['Subject', this.subject],
      ]
      if (this.imageLink) {
          headers.push(['Image', this.imageLink])
      }
      let content = buildRFC822(headers, this.newMessage)
      let response = await this.$http.post('/api/add-asset/', {filename: 'post.eml', content})
      let link = response.data
      await this.postMarkLink(link)
    },
    async postMarkLink(link) {
      let payload = msgpack.encode([this.$props.to, link])
      let v = msgpack.decode(payload)
      console.log(v)
      console.log(payload)
      let signature = sign(payload)
      let signer = getGraphId(await this.getSigner());
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
      if (!LOCKER) {
          console.log("WTF")
      }
      let pk = LOCKER.getKey().publicKey
      let ident = _.find(r.data.authUser.identities, {publicKey: pk})
      if (!ident) {
          ident = await this.registerIdentity()
      }
      return ident.id
    },
    async registerIdentity () {
      let signed_username = LOCKER.signedUsername()
      let public_key = LOCKER.getKey().publicKey
      console.log('su', signed_username)
      this.$data.key = public_key
      let response = await this.$apollo.mutate({
        mutation: REGISTER_IDENTITY,
        variables: {
            signedUsername: signed_username,
            publicKey: public_key,
        }
      })
      console.log('register response:', response)
      return response.data.registerIdentity.identity
    }
  }
}
</script>

<style scoped>
@import "~vue-wysiwyg/dist/vueWysiwyg.css";
</style>
