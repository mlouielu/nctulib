<template>
  <div id="search-input">
    <input placeholder="search your books" v-model="searchText" type="text" @keyup="search">
    <ul id="data">
      <li v-for="item in json">
        {{ item.author }}
      </li>
    </ul>
  </div>
</template>

<script>
import jquery from 'jquery'
import _ from 'lodash'

export default {
  name: 'hello',
  data () {
    return {
      searchText: '',
      json: ''
    }
  },
  methods: {
    search: _.debounce(function () {
      console.log(this.searchText)
      jquery.get('http://localhost:5000/books/' + this.searchText).then(response => {
        this.json = response
      })
    }, 1000)
  }
}
</script>
