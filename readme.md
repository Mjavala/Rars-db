## Local Development

To launch the postgres & hasura instances locally you must have docker installed and run the following command.

`` docker-compose up -d``

Then, you can visit the hasura console at ``localhost:8080``. Check the compose file for the HASURA_GRAPHQL_ADMIN_SECRET password to get in. In the hasura console under the data tab you'll find an SQL playground. Run the ``schema.sql`` file in the playground to generate the database schema. 

### Testing
Test data is provided in the ``test_data.json`` file which can be uploaded in the hasura console via the ``setup.sql`` file.

### Adding Data and Mocking Subscriptions
To add test data to the database run ``setup_py``.

You can then simulate the slide/box events by running ``sim.py``.

The simulation currently handles storage as three events.
- The staging area
- Boxed slide
- Box stored

Retrieval is the same, but in the opposite order.

## Graphql queries
On the home page of the Hasura console you'll find the exposed endpoint and graphQL playground. There's a lot of different queries that can be made, but here are some of the basic ones.

These queries can all be found in the ``sample_ui`` folder under the ``HelloWorld.vue`` component.

### slide infomation
```
    get_static_slide(slide) {
      this.$apollo.query({
        query: gql`query getslide($slide: String!) {
          slides(where: {SlideId: {_eq: $slide}}) {
            SlideId
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
```
### box information
```
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
```

### slide subscription
```
      get_slide: {
        query: gql`subscription getslide($slide: String!) {
          slides(where: {SlideId: {_eq: $slide}}) {
            SlideId
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
```

### box subscripton
```
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
```