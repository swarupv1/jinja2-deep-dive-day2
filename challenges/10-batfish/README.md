# Challenge - Batfish
 
The goal of this exercise is to learn about the common operations in Batfish. You will learn how to interact with Batfish and work with its output.
 
For certain parts of this challenge you will need to refer to https://pybatfish.readthedocs.io/en/latest/questions.html to understand the question that we will need to ask. 

## Exercise Overview
 
### Prerequisites
 
You will need to have:
* Python virtual environment created and activated
* the required dependencies installed
* a Batfish container running
* the example snapshot imported

```
docker pull batfish/allinone
docker run --name batfish -d -v batfish-data:/data -p 8888:8888 -p 9997:9997 -p 9996:9996 batfish/allinone

cd 10-batfish
virtualenv --python=`which python3` venv
pip3 install -r files/requirements.txt
source venv/bin/activate

./files/bf_snapshot_importer.py --snapshot_path files/nxos-spineleaf-001/
```

### Tasks
 
Submitting your solution for this challenge is optional - feel free to ask for help via email, chat, or at the open office hours if you get stuck!
 
#### Task 1 - Snapshot Import
 
From the helper file `bf_snapshot_importer.py` can you determine the line where the snapshot is initialized using the supplied snapshot path?

 
#### Task 2 - Snapshot Validation
 
Use Batfish to:
* obtain a parsing summary of the snapshot files.
* confirm the problematic configuration lines for each of the configurations. 

#### Task 3 - MTU Validation

Use Batfish to confirm the MTU for each of the interfaces within our snapshot.
 
#### Task 4 - OSPF Validation
 
Use Batfish to validate all OSPF adjacencies are correctly established. If they are not, please confirm reason.

 
