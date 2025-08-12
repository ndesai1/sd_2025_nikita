#!/usr/bin/env Rscript

rna_path      <- Sys.getenv("RNA_PATH", unset = NA)
variants_path <- Sys.getenv("VARIANTS_PATH", unset = NA)
coldata_path  <- Sys.getenv("COLDATA_PATH", unset = NA)
out_path      <- Sys.getenv("OUT_PATH", unset = NA)

if (any(is.na(c(rna_path, variants_path, coldata_path, out_path)))) {
  stop("run_etl.R expects RNA_PATH, VARIANTS_PATH, COLDATA_PATH, OUT_PATH")
}

read_csv <- function(p) {
  read.csv(p, header = TRUE, check.names = FALSE, stringsAsFactors = FALSE)
}

rna     <- read_csv(rna_path)
vars    <- read_csv(variants_path)
coldata <- read_csv(coldata_path)

# ---- RNA: per-sample mean across all genes ----
if (ncol(rna) < 2) stop("rna.csv must have gene names (col 1) + >=1 sample column")
sample_ids <- colnames(rna)[-1]

# TODO-1: numeric-coerce sample columns and compute mean across genes for each sample

# ---- Variants: per-sample burden from wide matrix ----
# Count non-empty, non-NA cells per sample column (exclude first 'gene' column)
if (ncol(vars) < 2) stop("variants.csv must have gene names (col 1) + >=1 sample column")
var_samples <- colnames(vars)[-1]
use_samples <- intersect(sample_ids, var_samples)

# TODO-2: for each sample in use_samples, count non-empty strings (not NA, not "")

# ---- colData join (uses 'sampleid') ----
if (!("sampleid" %in% names(coldata))) stop("colData.csv must include 'sampleid'")
keep <- intersect(c("sampleid"), names(coldata))
col_small <- unique(coldata[keep])

# Rename for join/output
names(col_small)[names(col_small) == "sampleid"] <- "sample_id"

# Build output table
out <- merge(rna_df, burden_df, by = "sample_id", all = TRUE)
out <- merge(out, col_small, by = "sample_id", all.x = TRUE)

# Order columns
want <- c("sample_id", "rna_mean", "variant_burden")
out <- out[intersect(want, names(out))]

dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
write.csv(out, out_path, row.names = FALSE)
