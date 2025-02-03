# qmbenchio
An open-source benchmark IO project.

![screenshot](docs/images/benchio_logo.png)

## Overview

* Develop a more comprehensive understanding of the relationships between quantum chemistry software, computing architecture, and simulation performance
* Investigation of storage technology impact on computation times on different scratch disk clusters

Our project begins with the utilization of OpenMOLCAS, a widely-acclaimed and extensively-used quantum chemistry software package, as part of the (ATTOP) project.

## Table of contents:

- [Requirements](#requirements)
- [Installation](#installation)
  - [Docker](#docker)
- [Getting Started](#getting-started)
- [About Us](#about-us)
- [Contributing to qmbenchio](/CONTRIBUTING.md)
- [Citing qmbenchio](#citing-qmbenchio)

## Installation
We recommend using Docker installation for reproducibility  

### Docker
```bash
docker build -t qmbhenchio .
```
```bash
docker start qmbenchio
```

## getting-started
A qmbenchio have 3 steps.
* Generate input data for qm software (for example openmolcas)
* Run on Cluster io benchmark using previously generated data
* Post processing of output file to generate Graph or report.

You can run all the step inside the docker container

The configurations of the directory path can be specified through a ini file. 
Examples of ini files can be found in config.ini.
```bash
cat /app/config.ini
```

>[Directories]
RawData=../data/raw_data/molcas_test
ProcessedData=../data/processed_data/molcas_test

run interactively inside the container
```bash
 docker exec -i -t qmbenchio /bin/bash
```

### First step : Generate the data

Example for openmolcas io 

```bash
cd /app/scripts
 python generate_molcas_io_job.py --openmolcas --jobs 1 10 --dir titi
```

The script take files in /app/data/raw_data and generate a titi bench with 1 job and 10 identical simultaneous job openmolcas IO input files. 

All files are generated in ProcessedData directory (cf config.ini) 

#### Example for openmolcas io bench :

    ├── processed_data/
    │   ├── molcas_test
    │     ├── titi
    │           ├──  job_1
    │                 ├──....
    │           ├── job_10
    │                  ├── ...
    └── ...

### Second step : Launch the jobs and generate output


### Third Step : Analyse the output and generate report or chart


## 📢  is under active development

