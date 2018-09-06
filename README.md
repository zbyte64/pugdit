# pugdit

A kind of bulletin board system with an emphasis on decentralization.
Posts are signed and exchanged between nodes.
Nodes act as moderators by ignoring or favoring posts for replication.
Policies work to optimize the "mail route" to weed out bad actors and favor nodes with worthy original content.


## Development

To get started with development, use docker compose:

    docker-compose build
    docker-compose create
    docker-compose start
    docker-compose run cli migrate
    docker-compose run cli createsuperuser
    docker-compose run cli mailcarrier


While the docker web service is running, also run the yarn dev service:

    cd pugboat
    yarn serve
