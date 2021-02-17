# MTG_Collection

## How to run dev

### 1. Install and start Docker

### 2. Start app
`docker-compose up --build`

### 3. Initialize database
Database is loaded from .rdb file in /mtg_collection/data/.  
If this file is missing, you need to init db first.  
* At first run, you need to download json file containing all mtg cards, you can do it by clicking 'Download data' button.
* After downloading file, initialize database by clicking 'Synchronize database' button.

## How does it work
TODO: Create collection -> add cards -> check prices etc.

## Backup
TODO: save to csv/json then import from that.

## Redis structure - TODO

Database currently contains all cards, all sets and all created collections.


key, value

cards
card:<edition>:<name>, <dictionary_values>

sets
edition:<edition>, <dictionary_values>

my collections
collection:<collection_name>, <collection_name>

My cards
<collection_name>:<name>, <dictinary_values>
