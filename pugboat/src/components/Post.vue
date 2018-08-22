<script>
import CorePost from './CorePost.vue'
import _ from 'lodash'

export default {
  name: 'Post',
  components: {
      CorePost
  },
  props: {
    post: !Object
  },
  render: function(createElement) {
    let makeTile = (post) => {
        let postElem = createElement(CorePost, {
            props: {
                post: this.post
            }
        })
        return createElement(
           'v-flex', {'class': {'xs4': true}}, [postElem]
        )
    }
    let makeTiles = (post) => {
        let tiles = [makeTile(post)]
        if (post.children) {
            tiles = _.concat(tiles, _.map(makeTiles, post.children))
        }
        return tiles
    }
    if (this.post.children) {
        let tiles = makeTiles(this.post)
        return createElement('template', tiles)
    } else {
        return makeTile(this.post)
    }
  }
}
</script>

<style scoped>

</style>
