# qmbenchio for benchmarking openmolcas IO

## Test Description

- Submission of calculations in a job array cluster to test the I/O limit using /scratch as temporary storage for files.
- Type of calculations: Single point CASSCF with OpenMolcas evaluating energies, gradients, and nonadiabatic coupling - 
Each subdirectory contains N copies of the same calculation (example : 1, 10, 100 ...) 
with an estimated disk space requirement of 500 MB per individual calculation and a total of 500 GB required for the test at 1000.

## Directory Content 

The Xjob directories contain X subdirectories named geometry, one for each calculation:
```
100job
|--geom_1
|--geom_2
...
|--geom_100
```

## Protocol
- A script submission script sub_molcas_nautilus_Xjob.sh is provided for each set.

- The script is configured to run a job array with X calculations, all writing to /scratch as temporary storage

-  Submit each individual script to test the speed of 1 calculation and single I/O on /scratch vs.
X calculations and X writes on /scratch.


Each geometry directory can contain the following files:

```
--geom_X
  |--geometry_1.xyz         #fichier xyz avec la géometrie moléculaire
  |--mol_input_1.input      #Input de molcas
  |--start.RasOrb           #Guess pour les orbitales moléculaires
  |
  |--mol_input_1.output     #Output du calculs molcas (contient le walltime)
  |--mol_input_1.status     #fichier contenant le message final du calcul ("Happy landing" si execution sans problème)
```

Le walltime et cputime sont dans les dernières lignes de mol_input_1.output

## Cleaning the tmp or scratch
it depends on the scratch storage cluster infrastructure (Here it's an Example on Glicid Cluster)
- All calculations write I/O to /scratch/waves/users/$USER/noRICD/X, where X corresponds to the number of calculations in the job array. Deleting /scratch/waves/users/$USER/noRICD allows for all cleanup.


