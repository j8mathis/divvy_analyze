.ktr files are pentaho data integration (kettle) files. The platform can be downloaded [here](https://sourceforge.net/projects/pentaho/files/Data%20Integration)

Below is a screenshot to show the tool. 

![pentaho_example](pentaho_example.png)

Kettle is a fantastic tool for pulling different data sources and performing analysis. Although a drag and drop tool it still has a decent learning curve. Kettle has the idea of jobs and transformations. Jobs are at a higher level and run steps sequentially. Some would say this is similar to a main function. You can create several different transformations and use a job to call each one in a particular order. Transformations run all the steps in parallel, so there is no guarantee one step will complete before another. Things such as setting variables would need to be set in a previous transformation and passed in at runtime. 

The above .ktr shows a quick example of the things you can do with kettle. There are several pentaho tools used for sorting, ranking, filtering, aggregating and even a little javascript. 
