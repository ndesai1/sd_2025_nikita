#!/usr/bin/env Rscript

# Strict, simple checks for the TCL38 wide-format CSVs.
# Env vars (set by Snakemake): RNA_PATH, VARIANTS_PATH, COLDATA_PATH, OUT_OK

rna_path      <- Sys.getenv("RNA_PATH", unset = NA)
variants_path <- Sys.getenv("VARIANTS_PATH", unset = NA)
coldata_path  <- Sys.getenv("COLDATA_PATH", unset = NA)
ok_out        <- Sys.getenv("OUT_OK", unset = NA)

if (any(is.na(c(rna_path, variants_path, coldata_path, ok_out)))) {
  stop("check_schema.R expects RNA_PATH, VARIANTS_PATH, COLDATA_PATH, OUT_OK")
}

read_csv <- function(p) {
  read.csv(p, header = TRUE, check.names = FALSE, stringsAsFactors = FALSE)
}

rna     <- read_csv(rna_path)
vars    <- read_csv(variants_path)
coldata <- read_csv(coldata_path)

# RNA: first column gene, >=1 sample column
if (ncol(rna) < 2) stop("rna.csv must have gene names (col 1) + >=1 sample column")

# Variants: must be wide like RNA: first column gene, >=1 overlapping sample column
if (ncol(vars) < 2) stop("variants.csv must have gene names (col 1) + >=1 sample column")

rna_samples <- colnames(rna)[-1]
var_samples <- colnames(vars)[-1]

overlap <- intersect(rna_samples, var_samples)
if (length(overlap) == 0) {
  stop("No overlapping sample columns between rna.csv and variants.csv")
}

# colData: must have 'sampleid'; 'group' is optional
if (!("sampleid" %in% colnames(coldata))) {
  stop("colData.csv must include 'sampleid'")
}

dir.create(dirname(ok_out), recursive = TRUE, showWarnings = FALSE)
cat("OK\n", file = ok_out)
