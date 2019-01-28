## Divvy Analyze Postgres

This example uses the divvy dataset with postgresql and sets up a good reporting foundation. Psycopg2 is used for connecting to postgresql and yaml files are used for configuring report runs. 

### Setup

#### Postgres Docker

I used a docker image for postgres db in this example. It was simple and met all my needs. Below are the steps to get it up and running. You will need to have docker installed; [instructions here.](https://docs.docker.com/install/)

[Postgres has an official image](https://hub.docker.com/_/postgres), you need to pull it onto your box. I used the latest which was 11.1. 

```bash
docker pull postgres
```

Next run the image, this will start the database server 

```bash
docker run --rm --name pg-docker -e POSTGRES_PASSWORD=pypgdemo -d -p 5432:5432 postgres
```

The "--rm" automatically removes the container when it exits. "--name" assigns a name to the container. "-e" sets an environment variable. "-d" runs the container detached in the background. "-p" forwards the port. 

Optionally you can also set a persistent volume with an option like this. The first directory needs to exist on your box. See comments in the issues section. 

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

You can run a sql file inside psql with a \i and a file path to the file. 
```bash
\i <path_to_query_file> 
```

#### venv

I used venv for this project, stepping away from pipenv. While pipenv has worked great, i felt it was overkill for the projects I was tackling. Virtual environment tooling in python has been quite confusing in the past few years. [Here is a link for tool recommendations from python.org.](https://packaging.python.org/guides/tool-recommendations/)

These steps will get you going

```bash
python3 -m venv env
source env/bin/activate
```

You should a "(env)" in the front of the command prompt now. Also notice where pip and python are pointing. 

```bash
which pip
which python
```

They should be pointing to <your project dir>/env/bin/python. Perfect. Now just run the install for the requirements file.

```bash
pip install -r requirements.txt
```

### the what

#### data loading

The data loading in this project was a snap. I decided to write a [bash script](https://github.com/j8mathis/divvy_analyze/blob/master/postgres/setup.sh) to use postgres' copy tools to move data from CSV to database table even though psycopg supported this functionality. The bash script did everything I needed it to in less than 40 lines. Create a database, tables, load data and even removed duplicates. Very nice and simple. It also did it in about 30 seconds. Compare that to a 4-5 day load into dynamodb and this database was moving at the speed of light. 

After the CSV files were loaded I moved on to the station data. I researched a few different ways to load this data. Load it into a jsonb column? Some kind of bulk load? Since its only 600 rows I decided to use psycopg ability to running an insert with named parameters. I could simply pass in a dict to a insert. beautiful. Loading the station data was no problem after that. 


#### data reporting

With the data neatly structured into tables, reporting was too easy. It was just a matter of running some sql queries. I didn't dig very deep into the queries, but the potential is there. I used a combination of psycopg and yaml files to run the reports. I like this approach because you can setup different attributes on the queries like name, description, etc. Also you can use different yaml files to run different sets of reports. Finally and more importantly you change the queries without touching the code. Which is nice for making tweaks on the reports. How many times does this happen in a workplace:) The foundation can really be built up from this point. 



#### issues
* Yaml - After I uploaded my initial commit I immediately got an email from github (thanks btw) about a security venerability in the version of pyyaml I was using. This lead to a lengthy history of web searches. Long story short the load() function could easily be exploited to run arbitrary code. Its getting fixed in the near future but you can also just use another funtion called safe_load().

* PyYaml is dead - There is some discussion online about this project being dead. There is this [fork](https://yaml.readthedocs.io/en/latest/overview.html), I don't know. Sticking with PyYaml for now since my needs are light. 

* Persistent storage for postgres docker - I initially tried this but the database got hung up quickly. Didn't investigate far but was probably due to the fact of it running on a laptop and not getting clean shutdowns. With data loads at about 30 seconds I didn't need this anyways. 

* JSON loading - I spent a fair amount of time trying to find good bulking loading method for this. I only had 600 rows so performance was not a concern, although the single inserts I imagine would get to be slow at scale.  I though about keeping the data in json and transforming the data inside the database. This could also open the possibility of collecting historical data for the stations on a daily or smaller increment. 

