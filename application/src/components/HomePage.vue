<template>
  <v-container
    class="container"
    style="height: 90%; width: 100%;"
  >
    <v-sheet
      color="white"
      elevation="5"
      rounded="lg"
      style="height: 100%; margin-left: 10%; margin-right: 10%;"
    >
      <v-row
        class="row pt-10"
        style="padding-left: 10%; padding-right: 10%;"
      >
        <v-text-field
          v-model="keyword"
          label="Keyword" 
          filled
          @keydown.enter="onSubmit"
        >
        </v-text-field>
        <v-btn 
          dark 
          large
          color="#4E73CC"
          @click="onSubmit"
          class="ml-2"
          style="margin-top: 0.55%;"
        > 
          Enter 
        </v-btn>
      </v-row>
      <v-row
        class="mt-0"
        style="padding-left: 10%; padding-right: 10%;"
      >
        <v-chip 
          v-for="word in keywords" :key="word"
          close
          close-icon="mdi-minus-circle"
          class="mr-1 ml-1 mt-1 mb-1"
          @click:close="removeKeyword(word)"
        >
          {{ word }}
        </v-chip>
      </v-row>
    </v-sheet>
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
    padding-left: 20%;
    padding-right: 20%;
  }
</style>
