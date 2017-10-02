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
    <div v-if="!onSearch" style="height: 70%; width: 100%; display: table">
      <div style="display: table-cell; vertical-align: middle;">
        <img id="nctu-logo" src="https://upload.wikimedia.org/wikipedia/zh/6/6b/NCTU_emblem.svg"></img>
        <h1>
          交大館藏搜尋
        </h1>
        <p style="font-style: italic; font-family: serif; font-size: 1.5em">
          - for Humans
        </p>
        <b-container>
          <b-row class="justify-content-md-center">
            <b-col cols="12" md="8" lg="5">
              <b-input-group id="first-search-bar">
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
              style="margin: 10px">
        <div>
          <div v-if="!locations[item.bid]" class="spinner-inner">
            <div class="double-bounce1"></div>
            <div class="double-bounce2"></div>
          </div>
          <b-row class="justify-content-md-center list-book-location">
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
        <b-button variant="outline-primary"
                  :href="'http://ustcate.lib.nctu.edu.tw/primo_library/libweb/action/display.do?tabs=detailsTab&ct=display&fn=search&doc=' + item.bid"
                  target="_new">
          Details
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
      if (!this.searchText) {
        return
      }
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

#nctu-logo {
  width: 30%;
  padding-bottom: 1em;
}

@media (max-width: 576px) {
  #ncut-logo {
    width: 20%;
  }
}

@media (min-width: 768px) {
  #nctu-logo {
    width: 15%;
  }
}

@media (min-width: 992px) {
  #nctu-logo {
    width: 15%;
  }
}

@media (min-width: 1200px) {
  #nctu-logo {
    width: 10%;
  }
}


@media screen and (min-width: 720px) {
  #first-search-bar {
    margin-left: 0.7em;
  }
}

.list-book-location {
  padding-top: 1em;
}

.list-book-location li {
  margin: 2px;
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
