# BloomBot Basestation

## About
This repository is for the software run on the BloomBot basestation. The basestation communicates with both the server and BloomBot. 

## Requirements
- Raspberry Pi
- NRF24 Radio

## Setup
[Install](https://realpython.com/installing-python/) Python and pip, then install the required packages.

```python
python -m pip install -r requirements.txt
```

### Environment Variables
An environment file should be provided in the root directory to properly configure the script. An example is included in the repo as [.env_example](.env_example).

## Deployment
An autostart script is provided as [start.sh](start.sh) which pulls the latest changes and installs requirements before starting the basestation.

## Changes
The main branch is protected from direct writes, ideally create a new branch to work in then merge it in with a pull request when ready.

If new packages are required, updated the requirements.txt file using pipreqs:

```python
pipreqs > requirements.txt --force
```