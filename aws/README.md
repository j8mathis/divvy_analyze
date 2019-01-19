### Divvy Analyze

TODO: Add a bunch of wording here :) 

Part #1 - data loading (complete)
Part #2 - reporting (not started)

#### Data flow

![aws_flow](aws_viz.png) 

#### Setup

I used pipenv for this project. The following snippets can get this started

```python
pip install pipenv #install pipenv if you don't have it
pipenv install #install packages from the Pipfile
pipenv shell #activate the pipenv shell

```


### Notes to write about
data loading was so sloooow - 10 batches (250) for 50 seconds 
known issues with data weirdness
slow count updates on table meta
not joining
not a good fit but was on the free tier


