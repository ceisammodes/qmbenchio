#!/bin/bash

#SBATCH --partition     standard
#SBATCH --qos           short
#SBATCH --job-name      SP
#SBATCH --nodes         1
#SBATCH --cpus-per-task 1
#SBATCH --mem           5000
#SBATCH --hint          nomultithread
#SBATCH --array         1
##SBATCH --nodelist      cloudbreak033,cnode313
source ~/.bashrc
module purge

module load openmolcas/current
micromamba activate /micromamba/CEISAM/envs/openmolcas

export TMPDIR="/scratch/waves/users/$USER/"

export SLURM_SUBMIT_DIR="$PWD"

export MOLCAS="/opt/software/glicid/applications/openmolcas/gitlab/build"

export MOLCAS_NPROCS="1"
export MOLCAS_MEM="4000"
export MOLCAS_REDUCE_PRT="NO"
export OMP_NUM_THREADS="1"
export NAME="mol_input_1"

#setenv MOLCAS_KEEP_WORKDIR NO
#setenv MOLCAS_PROJECT NAME
#setenv MOLCAS_OUTPUT NAME

echo $SLURM_JOB_NODELIST
export WorkDir="${TMPDIR}/noRICD/1/geom_${SLURM_ARRAY_TASK_ID}/"
mkdir -p $WorkDir

cd 1job/geom_${SLURM_ARRAY_TASK_ID}

cp ${SLURM_SUBMIT_DIR}/start.RasOrb ./

export MOLCAS_OUTPUT="${TMPDIR}/geom_${SLURM_ARRAY_TASK_ID}/"

python3 /opt/software/glicid/applications/openmolcas/gitlab/build/pymolcas ${SLURM_SUBMIT_DIR}/1job/geom_${SLURM_ARRAY_TASK_ID}/${NAME}.input >& ${SLURM_SUBMIT_DIR}/1job/geom_${SLURM_ARRAY_TASK_ID}/$NAME.output

#rm -r $WorkDir
