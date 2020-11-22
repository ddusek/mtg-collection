# MTG_Collection

## How to run

### 1. Fetch all cards json file.

`python main.py fetchcards`

### 2. Start redis
`redis-server redis.conf`

### 3. Fill database
Databases are loaded from .rdb files.  

If these files are missing, you need to init db first.  
`python main.py initdb`

### 4. Start dev vue app
in /frontend  
`npm run dev`

### 5. Start Flask
in /mtg_collection  
`export FLASK_APP=api/cards_api.py`  
`flask run --debugger`


Main database - dump_main.rdb.  
Collections databases - dump_<collection_name>.rdb.


### TODO
use generator for reading line by line  
dockerize app  
create all needed directories/files on init (logs dir)  
