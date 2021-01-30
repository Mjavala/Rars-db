## Local Development

To launch the postgres & hasura instances locally you must have docker installed and run the following command.

`` docker-compose up -d``

Then, you can visit the hasura console at ``localhost:8080``. Check the compose file for the HASURA_GRAPHQL_ADMIN_SECRET password to get in. In the hasura console under the data tab you'll find an SQL playground. Run the ``schema.sql`` file in the playground to generate the database schema. 

### Testing
Test data is provided in the ``test_data.json`` file which can be uploaded in the hasura console via the ``setup.sql`` file.

## Graphql queries
On the home page of the Hasura console you'll find the exposed endpoint and graphQL playground. There's a lot of different queries that can be made, but here are some of the basic ones.

### film infomation

### box information

### film subscription

### box subscripton (?)