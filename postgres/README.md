### Divvy Analyze Postgres

This example uses the divvy dataset with postgresql. I stay basic but set up a good foundation to be be built on. 

### Setup

#### Postgres Docker

I used a docker image for postgres db in this example. It was simple and met all my needs. Below are steps to get it up and running. You will need to have docker installed; [instructions here.](https://docs.docker.com/install/)

Pull postgres image

```bash
docker pull postgres
```

Next run the image 

```bash
docker run --rm --name pg-docker -e POSTGRES_PASSWORD=pypgdemo -d -p 5432:5432 postgres
```

The "--rm" automatically removes the container when it exits. "--name" assigns a name to the container. "-e" sets an environment variable. "-d" runs the container detached in the background. "-p" forwards the port. 

Optionally you can also set a persistent volume with an option like this. The first directory needs to exist on your box.

```bash
-v $HOME/docker/volumes/postgres:/var/lib/postgresql/data
```

For access into your new database, connect using your favorite db tool. If you don't have one, install psql. This a great commandline client for postgres. You will need the libpq package, its available on brew, apt, and yum installs. The name varies slightly. I am on macos so I used brew. 

```bash
brew install libpq
```

Finally login 
```bash
psql -h localhost -U postgres
```

keep going.....