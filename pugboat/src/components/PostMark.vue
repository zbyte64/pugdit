<template>
  <div class="post-mark">
    <v-radio-group v-model="postType">
      <v-radio label="Compose" value="newPost"/>
      <v-radio label="Image" value="newImage"/>
      <v-radio label="Link" value="link"/>
    </v-radio-group>
    <wysiwyg v-model="newMessage" v-if="postType == 'newPost'"/>
    <v-text-field v-model="link" v-if="postType == 'link'" label="existing IPFS link"/>
    <upload-btn :fileChangedCallback="uploadImage" v-if="postType == 'newImage'"></upload-btn>
    <v-btn
      @click="formValid && submit()"
    >Upload</v-btn>
  </div>
</template>

<script>
import POST_MARK from '../graphql/PostMark.gql'
import AUTH_SELF from '../graphql/AuthSelf.gql'
import {sign, decodeBase64} from '../mailbox.js'
import UploadButton from 'vuetify-upload-button';
import msgpack from 'msgpack-lite'


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
      switch(this.$data.postType) {
        case 'newPost':
          return this.newMessage
        case 'newImage':
          return this.link
        case 'link':
          return this.link
      }
      return false
    }
  },
  methods: {
    async submit() {
        switch(this.$data.postType) {
          case 'newPost':
            return await this.uploadMessage()
          case 'newImage':
            return await this.postMarkLink(this.link)
          case 'link':
            return await this.postMarkLink(this.link)
        }
    },
    async uploadImage(e) {
        console.log("upload", e)
        var formData = new FormData();
        formData.append('file', e);
        let response = await this.$http.post('/api/add-asset/', formData)
        let link = response.data
        await this.postMarkLink(link)
    },
    async uploadMessage () {
      if (!this.formValid) return
      //TODO indicate mimetype
      let response = await this.$http.post('/api/add-asset/', {filename: 'post', content:this.$data.newMessage})
      let link = response.data
      await this.postMarkLink(link)
    },
    async postMarkLink(link) {
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
      return r.data.authUser.identities[0].id
    }
  }
}
</script>

<style scoped>
@import "~vue-wysiwyg/dist/vueWysiwyg.css";
</style>
