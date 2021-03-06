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
        height="500"
        bench="5"
        item-height="64"
        class="list"
        id="vlist"
        :style="listHeight"
      >
        <template v-slot:default="{ item }">
          <v-list-item :key="item[1]">
            <v-list-item-action>
              <v-icon>mdi-file-document-outline</v-icon>
            </v-list-item-action>

            <v-list-item-content>
              <v-list-item-title>
                <strong>ID {{ item[0] }}</strong>
              </v-list-item-title>
            </v-list-item-content>

            <v-list-item-action>
              <v-btn
                icon
                @click="downloadFile(item)"
              >
                <v-icon small> mdi-download </v-icon>
              </v-btn>
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
      listHeight: "max-height: 70%;",
      rowHeight: 0,
      pMaxHeight: 70,
      files: []
    }),

    updated() {
      let newRowHeight = document.getElementById("keyrow").clientHeight;
        if (this.rowHeight - newRowHeight < 0) {
          this.pMaxHeight = Math.max(0, this.pMaxHeight - 5);
        }
        else if (this.rowHeight - newRowHeight > 0) {
          this.pMaxHeight = Math.max(0, this.pMaxHeight + 5);
        }

        this.listHeight = "max-height: " + this.pMaxHeight + "%;";
        this.rowHeight = newRowHeight;
    },

    methods: {
      getMatches: function() {
        this.$http.get("/matches", {
          params: {
            keyword: this.keyword,
            nsize: 3
          },
        })
        .then(response => response.data)
        .then(data => {
          this.files = [];
          data.files.forEach(file => this.files.push(file));
        });
      },

      onSubmit: function () {
        if (!this.keywords.includes(this.keyword) && this.keyword.length > 0) {
          this.keywords.push(this.keyword);
          this.getMatches();
        }
        this.keyword = "";
      },
      
      removeKeyword: function(word) {
        this.keywords = this.keywords.filter(k => k !== word);
      },

      downloadFile: function(fileData) {
        let file = fileData[0];
        let hash = fileData[1];

        this.$http.get("/file", {
          params: {
            hash: hash,
            filename: file
          },
        })
        .then(async response => {
          var fileURL = window.URL.createObjectURL(new Blob([response.data]));
          var fileLink = document.createElement('a');

          fileLink.href = fileURL;
          fileLink.setAttribute('download', file);
          document.body.appendChild(fileLink);

          fileLink.click();
        });
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
