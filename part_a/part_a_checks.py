## check mismatched sample IDs

#import data files:
import sys
import pandas as pd
from scipy import stats

### create option to input the path to the gene expression file:
###change this to argparse if there is time

gene_exp_filepath = sys.argv[1]
clin_data_filepath = sys.argv[2]

#gene_exp_filepath = "data/icb_gene_expression.csv"
#clin_data_filepath = "data/icb_clinical_data.csv"

gene_exp_data = pd.read_csv(gene_exp_filepath, header=0)

clin_data = pd.read_csv(clin_data_filepath)

#remove duplicates
clin_data = clin_data.drop_duplicates()

#### task 1: Check for mismatched sample IDs
gene_exp_IDs = list(gene_exp_data.columns[1:])
clin_data_IDs = list(clin_data['patientid'].dropna())

difference_1 = list(set(gene_exp_IDs)-set(clin_data_IDs))
difference_2 = list(set(clin_data_IDs)-set(gene_exp_IDs))

if len(difference_1):
    with open("qc_report.txt", 'w') as f:
        f.write(f"WARNING: The following samples are present in "
              f"{gene_exp_filepath} but not in {clin_data_filepath}:"
              f"{gene_exp_IDs}")
else:
    with open("qc_report.txt", 'w') as f:
        f.write(f"All samples in {gene_exp_filepath} are "
          f"in {clin_data_filepath}")


if len(difference_2):
    with open("qc_report.txt", 'w') as f:
        f.write(f"WARNING: The following samples are present in "
          f"{clin_data_filepath} but not in {gene_exp_filepath}:"
          f"{gene_exp_IDs}")
else:
    with open("qc_report.txt", 'w') as f:
        f.write(f"All samples in {clin_data_filepath} are "
          f"in {gene_exp_filepath}")


### task 2: Compute number of missing values in each dataset

# get number of missing fields for clinical data:
clin_data = clin_data[clin_data['patientid'].notna()]
clin_data['num_empty_fields'] = clin_data.isna().sum(axis=1)
total_fields = len(clin_data.columns) - 1
clin_data['percent_empty_fields'] = clin_data['num_empty_fields'] / total_fields

empty_field_patients = clin_data[clin_data['percent_empty_fields'] > 0.1]
empty_field_patients = list(empty_field_patients['patientid'])

with open("qc_report.txt", 'w') as f:
    f.write(f"Following patients have >10% empty fields in {clin_data_filepath}: "
            f" {empty_field_patients}")

gene_exp_data['num_empty_fields'] = gene_exp_data.isna().sum(axis=1)
total_fields_gene = len(gene_exp_data.columns) - 1
gene_exp_data['percent_empty_fields'] = gene_exp_data['num_empty_fields'] / total_fields_gene

with open("qc_report.txt", 'w') as f:
    f.write(f"Following patients have >10% empty fields in {gene_data_filepath}: "
            f" {empty_field_patients}")

### task 3: calculate mean expression of each gene across all samples

gene_exp_data['gene_mean_exp'] = gene_exp_data.iloc[:,1:].mean(axis=1)

# sort data and get top 5 genes:
gene_exp_data_sorted = gene_exp_data.sort_values(by=['gene_mean_exp'],
                                                 ascending = False)

top_5_gene_exp = gene_exp_data_sorted[['Unnamed: 0', 'gene_mean_exp']].head(5)
top_5_gene_exp.to_csv('top5_genes.csv', index=False)


# tast 4: merge expression and clinical data

gene_exp_data_t = gene_exp_data.transpose()
gene_exp_data_t.columns = gene_exp_data_t.iloc[0]

merged_data = pd.merge(clin_data, gene_exp_data_t,
                       left_on=clin_data.columns[0],
                       right_on=gene_exp_data_t.columns[0])

merged_data.to_csv('merged_data.csv', index=False)

#task 5

# Possible groups: gender, recist, age? (>50, <50)
# Compare gene expression by gender:
clin_data = clin_data[clin_data['patientid'].notna()]
female_patients = clin_data[clin_data['sex'] == 'F']['patientid']
male_patients = clin_data[clin_data['sex'] == 'M']['patientid']

gene_exp_data_female = gene_exp_data[gene_exp_data.columns.intersection(female_patients)]
gene_exp_data_female['genes'] = gene_exp_data['Unnamed: 0']
gene_exp_data_male = gene_exp_data[gene_exp_data.columns.intersection(male_patients)]

def t_test(sample_1, sample_2):
    t_statistic, p_value = stats.ttest_1samp(sample_1, sample_2)



