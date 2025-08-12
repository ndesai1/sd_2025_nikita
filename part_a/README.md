## Tasks

Write an R or Python script that does the following:

1. Check for mismatched sample IDs between expression and clinical data.
Expected output - A list of sample IDs present in one file (eg: Gene expression matrix) but not the other.

2. Compute the number of missing values in each dataset.
Expected output - Flag any samples with more than 10% missing clinical fields.

3. Calculate the mean expression of each gene across all samples.
Expected output - Return the top 5 most highly expressed genes.

4. Merge the expression and clinical data so that each row corresponds to a sample with both gene expression and clinical metadata.
Expected output - Keep only samples present in both datasets.

5. Simple Analysis-
From the clinical data, identify if there is a categorical variable (e.g., Response, Gender) that can be used for grouping.
Compare the mean expression of the top 5 genes between groups (e.g., responders vs. non-responders) using a t-test or Wilcoxon test.
Report the p-values.

6. Save files
