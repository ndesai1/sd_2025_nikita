## Tasks

Adjust the R scripts and Snakefile so that the following is fulfilled:

1. Given the broken Snakefile, fill in the correct fields to ensure the workflow is able to execute with the requirements
	- Add the correct code to activate the conda environment
	- set minimal viable threads
	- export correct environment variables to scripts
	- Ensure the snakefile runs E2E without error (If you're more comfortable using a makefile, you can convert the snakefile)
2. Fill in two TODO sections in scripts/run_etl.R to compute: 	  
	- rna_mean
	- variant_burden.
3. Join with colData to produce outputs/summary.csv with columns sample_id, rna_mean, variant_burden, ageAtSampling, sexOfCell, synonyms
4. If possible, package and run workflow inside a dockerized container that utilizes a package manager like conda for controlling the environment utilizing the .yaml file provided. Otherwise, run using solely a conda environment.
5. Describe what additional steps would you implement for reproducibility?