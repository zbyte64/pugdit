# pugdit

A kind of bulletin board system with an emphasis on decentralization.


## How it works

Discovers other peers over IPFS.
Once other peers are discovered, IPNS is used to locate a manifest of signed posts to be considered for replication.
Nodes act as moderators by ignoring or favoring posts for replication.
Policies work to optimize the "mail route" to weed out bad actors and favor nodes with worthy original content.


## Development

To get started with development, use docker compose:

    docker-compose up -d
    docker-compose run cli migrate
    docker-compose run cli createsuperuser
    docker-compose run cli mailcarrier


While the docker web service is running, also run the yarn dev service:

    cd pugboat
    yarn serve


### Folders

**pugboat** Vue client

**pugdit** Django server

The vue client is served as a SPA by Django. API calls are made using GraphQL.


### Nexus

An IPFS node that is publishing using pugdit. Often referred to as a node in this project.

### Identities

Identities are one-to-one with elliptic signing keys. 
A node may associate multiple identities to a single account, representing different signing sources of the same user.


### Signed Posts

A post is comprised of a `to` address and an IPFS `link`. 
A signed post is a message packed tuple of those values signed by an identity.
To display a post nicely, they are formatted as rfc2822.


### Manifests

Manifests are message packed dictionaries of signed messages and identity public keys.
A node may accept or reject new identities from another node.

### Karma

Every node, post, and identity has associated karma.
Nodes with negative karma will not accept new identities.
Identities with large negative karma will not have their posts accepted.
TODO: more to come.
