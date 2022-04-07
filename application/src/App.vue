<template>
  <v-app>
    <v-main 
      class="root"
    >
      <HomePage/>
    </v-main>
  </v-app>
</template>

<script>
import HomePage from './components/HomePage';

export default {
  name: 'App',

  components: {
    HomePage,
  },

  data: () => ({
    //
  }),
};
</script>

<style lang="scss">
  .root {
    background-image: linear-gradient(90deg, #6D12C6, #2876F8);
  }
</style>
