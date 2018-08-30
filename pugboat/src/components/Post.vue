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
    let makeTile = (post, classes) => {
        let postElem = createElement(CorePost, {
            props: {
                post: this.post
            }
        })
        return createElement(
           'v-flex', {'class': classes || {xs4: true}}, [postElem]
        )
    }
    let makeTiles = (post, classes) => {
        let tiles = [makeTile(post, classes)]
        if (post.children) {
            tiles = _.concat(tiles, _.map(makeTiles, post.children))
        }
        return tiles
    }
    if (this.post.children) {
        let tiles = makeTiles(this.post, this.classes)
        if (tiles.length == 1) return tiles[0]
        if (tiles.legnth == 0) return null
        return createElement('div', tiles)
    } else {
        return makeTile(this.post, this.classes)
    }
  }
}
</script>

<style scoped>

</style>
