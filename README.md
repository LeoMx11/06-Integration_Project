
# Integrating Bulk RNA-seq Data to Genome Pipeline

### By Leo McMahon

This pipeline outlines how to go from raw bulk RNA-seq reads, in this case drawn from the NCBI Sequence Read Archive (SRA) using the SRA Toolkit.

In using this pipeline, different projects will have to start at different steps. For example, if you already have your .fastq files ready from another source other than SRA, you can obviously skip the first step of downloading the .fastq files from NCBI.

Additionally, in using the MASTERPROCESS file, all of the necessary steps will be executed sequentially with no outside input from the user. However, if you only want to use one of the steps, the individual files will also be included so that a step-by-step process can be used if necessary.

## Step 1A: Collect your data

If you already have your .fastq files, skip this step. But if you are accessing your files from the NCBI SRA, follow this step.

The general steps for downloading and utilizing the SRA toolkit are here: https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit.

For my fellow UCSB Pod users however, I will outline exactly what I did on my computer to get this to work on the Pod.


