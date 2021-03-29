## The Challenge
We need to download movies data, do some transformation and insert into the db. Then any BI/analytics
tool can extract those data to show it in beautiful charts. This should also be reproducible and automated. The problem that we are solving with
this assignment are:  

* Orchestration : *We need to run it as scheduled tasks so cron or tool has to be used.*
* Transforamation(Processing): *Data will be huge so good language and script has to be used.*
* Storage: *The dump and csv files are big so a good approach should be taken to store and retrive .*

## The Design
The problems defined above are similar kind of challenges that the world is facing with increasing amount of data, transformation
and processing. The approach would be to build a pipeline completely using cloud solutions like a cloud storage, a cloud hosted airflow , serverless db and any BI tool.
For this assignment we will do a compact version of it which can be run locally and can be enhanced to run on any cloud.
![Alt text](design.png?raw=true "Design")

## Language Tools Used
* Python 3.7 (Anaconda)
* Docker
* Apache Airflow
* Postgre
* Pycharm IDE(Any IDE will work)


## Why Specific tools are choosen
* Airflow : It does the same like a blunt cron but can be scaled to thousands of tasks, GUI with easy to trace logs and simple.
* Python : Easy to use scripting language with different libs for big data analysis.
* Docker : Helps to containerize everything so that apps can be scaled, reproduced and easily deployed on dev, test and prod.
* Postgre : Open source db which cab be easily scaled.
* Pytest : Pytest is used for the unit testing,

## The Implementation & Steps to Run
* Airflow is the core of the processing in our case.
* It downloads the xml and csv files.
* Initiates the processing
* Inserts the data into csv

### Steps to Run
```git clone 
cd cd tl-data-eng-interview
docker-compose up --build
```

Open up url http://0.0.0.0:8080 in the browser and on the left top corner start. The whole job is scheduled to run hourly
but can be change accordingly. 


## The Testing
As testings are lines of defence for any application so we are splitting them into
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
 
 ## Area of Improvement
I can see few places that could have been better.(The time is what is required).
* Data could be downloaded to cloud and store as splitted file instead of big file.
* A spark processing could be a better option once the file becomes bigger.
* A cloud bigdata service like EMR job could be directly initiated from airflow.
* Services could be moved to K8 for better container management.





