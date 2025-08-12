#!/bin/bash
#SBATCH --job-name=test
#SBATCH --nodes=10
#SBATCH --ntasks=40
#SBATCH --time=1:00:00
#SBATCH --mem=200M
module load R
Rscript non_existent_script.R
