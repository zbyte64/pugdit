<script>
export default {
  name: 'Avatar',
  props: {
    user: !Object
  },
  render: function(createElement) {
    if (this.user.email) {
        return createElement('v-gravatar', {props: {email: this.user.email}})
    }
    return createElement('v-gravatar', {props: {hash: this.user.publicKey}})
  }
}
</script>

<style scoped>

</style>
