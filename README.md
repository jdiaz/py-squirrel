PySquirrel
==========

Dynamically create an SQL script backup of a database.

### Usage

1. Run ```pip install mysql-connector-python```
2. Configure the DB object with appropriate db connection information
3. Run ```./pysquirrel```

Open / Run the `DATABASE_NAME.sql` produced. The file contains all relevant SQL statements to recreate and insert each record in the database.

** Currently under development **