<template>
    <v-container fluid grid-list-lg>
      <v-slide-y-transition>
        <v-layout row wrap>
          <FrontPosts/>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
import FrontPosts from '../components/FrontPosts.vue';

export default {
    components: {
        FrontPosts
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
