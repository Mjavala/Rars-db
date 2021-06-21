## Local Development
To launch the postgres & hasura instances locally you must have docker installed and run the following command.\
`` docker-compose up -d``
Then, you can visit the hasura console at ``localhost:8080``. Check the compose file for the HASURA_GRAPHQL_ADMIN_SECRET password to get in.\
\
To set up the empty database with the current schema, run the setup file with:\
\
```poetry run python setup.py```

You can modify this file to insert any of the test data json files. At this point you'll have a set up for testing.

### API Endpoints
This section is under development.
- **get_slide** (POST)
```
request:
{
  "payload": "KL20-12031_B_2.35.1"  # String
}
response:
{
  "slideid": "KL20-12031_B_2.35.1",
  "blockid": "KL20-12031_B_2",
  "accessionid": "KL20-12031",
  "stain": "H&E",
  "stainorderdate": "2020-09-08 15:22:36",
  "sitelabel": "MAWD",
  "casetype": "KL",
  "year": "20",
  "ts": "1624179320.740725",
  "location": "5",
  "retrievalrequest": None,
  "requestedby": None,
  "requestts": None,
  "box_id": "Box1",
}
```


### Testing
In order to run the integration tests in the ``/tests`` directory, first spin up the flask app with:\
```poetry run python main.py```\
\
Then you can run the pytest command to test the integration between the API and database.

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
