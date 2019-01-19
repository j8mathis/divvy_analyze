### Divvy Analyze

To summarize what this does: 

* Get data from a http end point
* Pull data from compressed folder
* Create data frames and join them together
* Run a few different aggregations on the combined data


### Setup

I used pipenv for this project. The following snippets can get this started

```python
pip install pipenv #install pipenv if you don't have it
pipenv install #install packages from the Pipfile
pipenv shell #activate the pipenv shell

```

### Thoughts
I liked this approach. It was quick, fairly easy, and no other infrastructure was needed. Just run the code and you get your answer. Data could live in S3 or another object storage. Although I see the advantage to just loading this into a db and being able to query and tweak the data to your liking. I will go over this in the postgresql example. Overall a very useful tool, I can see why pandas and numpys are so popular and I could get use to using them all the time.