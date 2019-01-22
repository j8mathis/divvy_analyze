### Divvy Analyze

This was an experimental learning experience. I really enjoyed this approach. It was quick, fairly easy, and no other infrastructure was needed. Just run the code and you get your answer. Compare this to waiting days for data loading into a database instead of getting the answer right away was a huge win. Overall a very useful tool, I can see why pandas and numpys are so popular and I could get use to using them all the time.

### What

This does the same basic flow as the other examples:

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
If you use this code stack daily or at least frequently, the benefits would be tremendous. Quickly being able to process multiple different data sources, joining them together, running calculations and spitting out an answer. As simple as that sounds its also a powerful thing. 