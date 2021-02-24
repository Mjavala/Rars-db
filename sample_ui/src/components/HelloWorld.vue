<template>
  <div id="wrapper">
    <h1>Rars Sample UI</h1>
    <main id="main">
      <div id="object_wrappers">
        <h3>slide Info</h3>
        <pre id="static_slide" />
        <pre id="socket_slide" />
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
      static_slide_name: 'TEST_slide_STATIC',
      socket_slide_name: 'TEST_slide_SOCKET',
      static_box_name: 'TEST_BOX_STATIC',
      socket_box_name: 'TEST_BOX_SOCKET',

      data: null
    }
  },
  apollo: {
    $subscribe: {
      get_slide: {
        query: gql`subscription getslide($slide: String!) {
          slides(where: {slide_id: {_eq: $slide}}) {
            slide_id
            box_id
            location
            ts
          }
        }`,
        variables () {
          return {
            slide: this.socket_slide_name
          }
        },
        result ({data}){
          this.addToFeed(data, 'socket_slide')
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
    this.get_static_slide(this.static_slide_name)
    this.$apollo.subscribe.get_slide
  },
  methods: {
    get_static_slide(slide) {
      this.$apollo.query({
        query: gql`query getslide($slide: String!) {
          slides(where: {slide_id: {_eq: $slide}}) {
            slide_id
            box_id
            location
            ts
          }
        }`,
        variables: {
          slide
        }
      }).then((response) => {
        console.log(response)
        this.data = response.data.slides[0]
        this.addToFeed(this.data, 'static_slide')
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
