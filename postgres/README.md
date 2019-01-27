### Divvy Analyze Postgres

This example uses the divvy data with postgresql. This example stays basic but set up a good foundation to be be built on. 

### Setup

#### Postgres Docker

I used a docker image for postgres db in this example. It was simple and met all my needs. Below are steps to get it up and running. 

Pull postgres image

```bash
docker pull postgres
```

Next run the image and you are up 

```bash
docker run --rm --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 
```

The "--rm" automatically removes the container when it exits. "--name" assigns a name to the container. "-e" sets an environment variable. "-d" runs the container detached in the background. "-p" forwards the port. 

Optionally you can also set a persistent volume with an option like this

```bash
-v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres
```

For access into your new database connecting using your favorite gui db tool. Or you can install psql which is a great commandline client for postgres. You need the libpq package its available on brew, apt, yum installs. THe vary slightly. I am on macos so I used brew. 

```bash
brew install libpq
```

Finally login 
```bash
psql -h localhost -U postgres -d postgres
```

keep going.....