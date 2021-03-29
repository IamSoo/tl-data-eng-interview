## The Challenge
We need to download movies related data, do some transformation and insert the result into the db. Then any BI/analytics
tool can extract those data to show it in beautiful charts. This should also be reproducible and automated. The problem that we are solving with
this assignment are:  

* Orchestration : *We need to run the job as a scheduled task, so a cron job or a tool with cron feature has to be used.*
* Transformation(Processing): *Data will be huge so good language with efficient libraries has to be used.*
* Storage: *The dump and csv files are pretty big a good approach should be taken to store and process them .*

## The Design
The problem defined above is a similar challenge that the many applications are facing to tackle increasing amount of data, transformation
and processing. The approach would be to build a pipeline completely using cloud solutions like a cloud storage, a cloud hosted airflow , serverless db and any BI tool.
For this assignment we will design a compact version of it which can be run locally and can be enhanced to run on any cloud.
![Alt text](design.png?raw=true "Design")

## Pre-requisite
Pipenv: Virtual env for python https://pypi.org/project/pipenv/  
Git: Source control to store our code https://git-scm.com/book/en/v2/Getting-Started-Installing-Git and open an account.    
Python: A programming language, quite popular for data analytics https://www.python.org/downloads/

## Language Tools Used
* Python 3.7 (Anaconda)
* Docker
* Apache Airflow
* Postgre
* Pycharm IDE(Any IDE will work)
* Any IDE to use a database client. Command line tool with postgre plugins will also work.


## Why Specific tools are choosen
* Airflow : It does the same like a blunt cron but can be scaled to thousands of tasks, GUI with easy to trace logs and simple.
* Python : Easy to use scripting language with different libs for big data analysis.
* Docker : Helps to containerize everything so that apps can be scaled, reproduced and easily deployed on dev, test and prod.
* Postgre : Open source db which cab be easily scaled.
* Pytest : Pytest is used for the unit testing,

## The Implementation & Steps to Run
* Airflow is the heart of the processing in our case.
* It downloads the xml and csv files.
* Initiates the processing.
* Also inserts the data into db.

We use docker-compose which installs multiple containers and tie them together. We use apache-airflow image which installs all its
dependency. We also install another postgre to use it as our database.

### Steps to Run
```
git clone git@github.com:IamSoo/tl-data-eng-interview.git
cd tl-data-eng-interview
docker-compose up --build
```

Open up the url http://0.0.0.0:8080 in a browser. We can see an apache airflow web ui. The whole job is scheduled to run hourly
but can be change accordingly. Click on the DAGs option to see configured DAGs.


## The Testing
As testings are the lines of defence for any application so we are splitting them into
* Unit Testing:  
   * Unit test each dag about their existance.
   * Dag integrity test to verify if dags are properly written and dont have any syntax errors.
* Functional Test:
    * Test operators to look into functionality.
    * Check if data frames are created with proper data format.
* Integration:
    * This is a bit tricky and has to be done by mocking as airflow consits of lots of small chunks of work
    which interact to storage, net, db independently. This part is not convered.

### Steps to run
```buildoutcfg
cd tl-data-eng-interview
pytest
```

## Verify
Connect to the postgres db with user:postgres, password:postgres, db:postgres, port:5432 and query the report table. (This is for dev only  
credentials will be never hardcoded or shared. Normally those are passed as environment parameters.)

```buildoutcfg
select * from movie_report
```

 
 ## Areas of Improvement
I can find places which could have been done better.(The time is everything required to achieve that).
* Data could be downloaded to any cloud storage and and could have been splitted for processing instead of using a big file.
* A spark processing could be a better option once the file becomes bigger.
* Hosted bigdata service like an EMR job could be directly initiated from airflow.
* Services could be moved to K8 for better container management and orchestration.





