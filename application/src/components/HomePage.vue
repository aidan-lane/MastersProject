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
        class="row-pad pt-10"
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
        id="keyrow"
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
      <v-virtual-scroll
        :items="files"
        height="550"
        bench="5"
        item-height="64"
        max-height="90%"
        class="list"
        id="vlist"
      >
        <template v-slot:default="{ item }">
          <v-list-item :key="item">
            <v-list-item-action>
              <v-btn
                fab
                small
                depressed
                color="primary"
              >
                {{ item }}
              </v-btn>
            </v-list-item-action>

            <v-list-item-content>
              <v-list-item-title>
                User Database Record <strong>ID {{ item }}</strong>
              </v-list-item-title>
            </v-list-item-content>

            <v-list-item-action>
              <v-icon small>
                mdi-open-in-new
              </v-icon>
            </v-list-item-action>
          </v-list-item>

          <v-divider></v-divider>
        </template>
      </v-virtual-scroll>
    </v-sheet>
  </v-container>
</template>

<script>
  export default {
    name: 'HomePage',

    data: () => ({
      keyword: "",
      keywords: [],
      selectedFile: "",
      listHeight: 550,
      newHeight: 550,
      files: ["haha", "hehe", "123", "tdtwtdwdw", "dwdwd", "dwdwwd", "dwdwwd", "hehe", "123", "tdtwtdwdw", "dwdwd", "dwdwwd", "dwdwwd"]
    }),

    mounted () {
      this.listHeight = document.getElementById("vlist").clientHeight;
    },

    methods: {
      onSubmit: function () {
        if (!this.keywords.includes(this.keyword) && this.keyword.length > 0) {
          this.keywords.push(this.keyword);
          self.newHeight = "max-height: " + parseFloat((this.listHeight - document.getElementById("keyrow").clientHeight) / this.listHeight * 100).toFixed(2)+"%;";
          console.log("test",  self.newHeight)
        }
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

  .row-pad {
    padding-left: 20%;
    padding-right: 20%;
  }

  .list {
    margin-left: 10%;
    margin-right: 10%;
    margin-top: 30px;
  }
</style>
