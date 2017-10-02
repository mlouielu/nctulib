<template>
  <div id="search">
    <div id="search-input" v-if="onSearch">
      <b-input-group>
        <b-form-input v-model="searchText"
                    type="text"
                    size="lg"
                    v-on:keyup.enter.native="search"
                    placeholder="The resource you want to search"></b-form-input>
        <b-input-group-button slot="right">
          <b-btn size="lg" variant="info" v-on:click="search">Search</b-btn>
        </b-input-group-button>
      </b-input-group>
    </div>
    <div v-if="!onSearch" style="height: 100%; width: 100%; display: table; margin-top: -10em">
      <div style="display: table-cell; vertical-align: middle;">
        <img width="20%" src="https://upload.wikimedia.org/wikipedia/zh/6/6b/NCTU_emblem.svg"
             style="padding-bottom: 2em"></img>
        <h1>
          交大館藏搜尋
        </h1>
        <p style="font-style: italic">
          - for Humans
        </p>
        <b-container>
          <b-row class="justify-content-md-center">
            <b-col cols="12" md="6" lg="4">
              <b-input-group>
                <b-form-input v-model="searchText"
                            type="text"
                            v-on:keyup.enter.native="search"
                            placeholder="The resource you want to search"></b-form-input>
                <b-input-group-button slot="right">
                  <b-btn variant="info" v-on:click="search">Search</b-btn>
                </b-input-group-button>
              </b-input-group>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
    <div v-if="searching" class="spinner">
      <div class="double-bounce1"></div>
      <div class="double-bounce2"></div>
    </div>
    <div style="padding-top: 20px">
      <b-card :title="item.title"
              :sub-title="item.author"
              v-bind:id="item.bid"
              v-for="item in json"
              v-observe-visibility="get_book_locations"
              style="margin: 5px">
        <div>
          <div v-if="!locations[item.bid]" class="spinner-inner">
            <div class="double-bounce1"></div>
            <div class="double-bounce2"></div>
          </div>
          <b-row class="justify-content-md-center">
            <b-col cols="12" md="8" lg="4">
              <ul style="list-style-type: none; display: block; text-align:left; padding-left: 0;">
                <li v-for="location in locations[item.bid]" v-model="locations[item.bind]"
                    style="text-indent: -1rem; padding-left: 2rem">
                  <i v-if="location.available == '有可用館藏'" class="fa fa-check" style="color: #43926a"></i>
                  <i v-else class="fa fa-times" style="color: #AC1D22"></i>
                  {{ location.library }} - {{ location.floor }}: {{ location.cite }}
                </li>
              </ul>
            </b-col>
          </b-row>
        </div>
        <b-button :size="lg" variant="outline-primary">
          <a href="#">Details</a>
        </b-button>

      </b-card>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import jquery from 'jquery'

export default {
  name: 'hello',
  data () {
    return {
      onSearch: false,
      searching: false,
      searchText: '',
      json: '',
      locations: {},
      fields: [
        {key: 'available', label: 't'},
        'cite',
        'floor',
        'library'
      ]
    }
  },
  methods: {
    search: function () {
      this.onSearch = true
      this.json = ''
      this.locations = {}
      this.searching = true
      jquery.get('https://nctulib.louie.lu/api/books/' + this.searchText).then(response => {
        this.json = response
        this.searching = false
      })
    },
    get_book_locations: function (isVisible, entry) {
      console.log(isVisible, entry.target.id)
      if (isVisible && !this.locations[entry.target.id]) {
        jquery.get('https://nctulib.louie.lu/api/location/' + entry.target.id).then(response => {
          Vue.set(this.locations, entry.target.id, response)
        })
      }
    }
  }
}
</script>

<style>
#search {
  height: 100%;
}

#search-input input {
  border-radius: 0;
}

#search-input button {
  border-radius: 0;
}

@media screen and (max-width: 600px) {
  #bk {
    background-image: url(https://upload.wikimedia.org/wikipedia/zh/6/6b/NCTU_emblem.svg);
    background-repeat: no-repeat;
    background-position: 50% 25%;
    background-size: 28%;
  }
}

@media screen and (max-width: 1200px) {
  #bk {
    background-image: url());
    background-repeat: no-repeat;
    background-position: 50% 28%;
    background-size: 15%;
  }
}

@media screen and (max-width: 1600px) {
  #bk {
    background-image: url(https://upload.wikimedia.org/wikipedia/zh/6/6b/NCTU_emblem.svg);
    background-repeat: no-repeat;
    background-position: 50% 23%;
    background-size: 12%;
  }
}

@media screen and (min-width: 1600px) {
  #bk {
    background-image: url(https://upload.wikimedia.org/wikipedia/zh/6/6b/NCTU_emblem.svg);
    background-repeat: no-repeat;
    background-position: 50% 25%;
    background-size: 8%;
  }
}



.spinner {
  width: 40px;
  height: 40px;

  position: relative;
  margin: 100px auto;
}

.spinner-inner {
  width: 10px;
  height: 10px;

  position: relative;
  margin: 10px auto;
}

.double-bounce1, .double-bounce2 {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: #333;
  opacity: 0.6;
  position: absolute;
  top: 0;
  left: 0;

  -webkit-animation: sk-bounce 2.0s infinite ease-in-out;
  animation: sk-bounce 2.0s infinite ease-in-out;
}

.double-bounce2 {
  -webkit-animation-delay: -1.0s;
  animation-delay: -1.0s;
}

@-webkit-keyframes sk-bounce {
  0%, 100% { -webkit-transform: scale(0.0) }
  50% { -webkit-transform: scale(1.0) }
}

@keyframes sk-bounce {
  0%, 100% {
    transform: scale(0.0);
    -webkit-transform: scale(0.0);
  } 50% {
    transform: scale(1.0);
    -webkit-transform: scale(1.0);
  }
}
</style>
