#!/bin/bash
## TEMPLATE QMBENCHIO 1JOB FOR GLICID CLUSTER
#SBATCH --partition     standard
#SBATCH --qos           short
#SBATCH --job-name      SP
#SBATCH --nodes         1
#SBATCH --cpus-per-task 1
#SBATCH --mem           5000
#SBATCH --hint          nomultithread
#SBATCH --array         1-{REMPLACE_NJOB}
##SBATCH --nodelist      cloudbreak[033-034]
source ~/.bashrc
module purge

module load openmolcas/current
micromamba activate /micromamba/CEISAM/envs/openmolcas

export TMPDIR="/scratch/nautilus/users/$USER/"

export SLURM_SUBMIT_DIR="$PWD"

export MOLCAS="/opt/software/glicid/applications/openmolcas/gitlab/build"

export MOLCAS_NPROCS="1"
export MOLCAS_MEM="4000"
export MOLCAS_REDUCE_PRT="NO"
export OMP_NUM_THREADS="1"
export NAME="mol_input_1"

export WorkDir="${TMPDIR}/noRICD/{REMPLACE_NJOB}/geom_${SLURM_ARRAY_TASK_ID}/"
mkdir -p $WorkDir

cd {REMPLACE_NJOB}job/geom_${SLURM_ARRAY_TASK_ID}

cp ${SLURM_SUBMIT_DIR}/start.RasOrb ./

export MOLCAS_OUTPUT="${TMPDIR}/geom_${SLURM_ARRAY_TASK_ID}/"

python3 /opt/software/glicid/applications/openmolcas/gitlab/build/pymolcas ${SLURM_SUBMIT_DIR}/{REMPLACE_NJOB}job/geom_${SLURM_ARRAY_TASK_ID}/${NAME}.input >& ${SLURM_SUBMIT_DIR}/{REMPLACE_NJOB}job/geom_${SLURM_ARRAY_TASK_ID}/$NAME.output

#rm -r $WorkDir
