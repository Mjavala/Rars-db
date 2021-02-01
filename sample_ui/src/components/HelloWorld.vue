<template>
  <div id="wrapper">
    <h1>Rars Sample UI</h1>
    <main id="main">
      <div id="object_wrappers">
        <h3>Film Info</h3>
        <pre id="static_film" />
        <pre id="socket_film" />
      </div>
      <div id="object_wrappers">
        <h3>Box Info</h3>
        <pre id="static_box" />
        <pre id="socket_box" />

      </div>
    </main>
  </div>
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: 'HelloWorld',
  data () {
    return {
      static_film_name: 'TEST_FILM_STATIC',
      socket_film_name: 'TEST_FILM_SOCKET',
      static_box_name: 'TEST_BOX_STATIC',
      socket_box_name: 'TEST_BOX_SOCKET',

      data: null
    }
  },
  apollo: {
    $subscribe: {
      get_film: {
        query: gql`subscription getFilm($film: String!) {
          films(where: {film_id: {_eq: $film}}) {
            film_id
            box_id
            location
            ts
          }
        }`,
        variables () {
          return {
            film: this.socket_film_name
          }
        },
        result ({data}){
          this.addToFeed(data, 'socket_film')
        }
      },
      get_box: {
        query: gql`subscription getBox($box: String!) {
          boxes(where: {box_id: {_eq: $box}}) {
            box_id
            cabinet_id
            ts
          }
        }`,
        variables () {
          return {
            box: this.socket_box_name
          }
        },
        result ({data}){
          this.addToFeed(data, 'socket_box')
        }
      }
    }
  },
  mounted () {
    this.get_static_box(this.static_box_name)
    this.get_static_film(this.static_film_name)
    this.$apollo.subscribe.get_film
  },
  methods: {
    get_static_film(film) {
      this.$apollo.query({
        query: gql`query getFilm($film: String!) {
          films(where: {film_id: {_eq: $film}}) {
            film_id
            box_id
            location
            ts
          }
        }`,
        variables: {
          film
        }
      }).then((response) => {
        console.log(response)
        this.data = response.data.films[0]
        this.addToFeed(this.data, 'static_film')
      })
    },
    get_static_box(box) {
      this.$apollo.query({
        query: gql`query getBox($box: String!) {
          boxes(where: {box_id: {_eq: $box}}) {
            box_id
            cabinet_id
            ts
          }
        }`,
        variables: {
          box
        }
      }).then((response) => {
        console.log(response)
        this.data = response.data.boxes[0]
        this.addToFeed(this.data, 'static_box')
      })
    },
    addToFeed (message, target) {
      const feed = document.getElementById(target)
      feed.innerHTML = JSON.stringify(message, undefined, 4)
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #wrapper {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    flex-direction: column;
  }
  #main {
    height: 100%;
    width: 100%;
    display: flex;
    flex: 1;
  }
  #object_wrappers {
    height: 100%;
    width: 100%;
    flex: 1;
  }
  h1 {
    padding: 1em;
  }
</style>
