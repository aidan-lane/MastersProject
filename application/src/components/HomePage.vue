<template>
  <v-container
    class="container"
  >
    <v-row
      class="row"
    >
      <v-text-field
        v-model="keyword"
        label="Keyword" 
        solo
        @keydown.enter="onSubmit"
      >
      </v-text-field>
      <v-btn 
        dark 
        large
        color="blue"
        @click="onSubmit"
        class="ml-2"
        style="margin-top: 3px;"
      > 
          Enter 
      </v-btn>
    </v-row>
    <v-row
      class="mt-0"
    >
      <v-chip 
        v-for="word in keywords" :key="word"
        close
        close-icon="mdi-close-outline"
        class="mr-1 ml-1 mt-1 mb-1"
        @click:close="removeKeyword(word)"
      >
        {{ word }}
      </v-chip>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'HomePage',

    data: () => ({
      keyword: "",
      keywords: []
    }),

    methods: {
      onSubmit: function () {
        if (!this.keywords.includes(this.keyword) && this.keyword.length > 0)
          this.keywords.push(this.keyword);
        this.keyword = "";
      },
      
      removeKeyword: function(word) {
        this.keywords = this.keywords.filter(k => k !== word);
      }
    }
  }
</script>

<style lang="scss">
  .container {
    margin-top: 50px;
  }

  .row {
    padding-left: 10%;
    padding-right: 10%;
  }
</style>
