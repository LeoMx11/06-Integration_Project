import os
import subprocess

# Directories
base_dir = "/home/leomcmahon/06-Integration_Project-main/3-TRIM/processed_FASTQ"
cds_fasta = "/home/leomcmahon/06-Integration_Project-main/4-MAP/bs_primary_asm.fa"
annotation_gtf = "/home/leomcmahon/06-Integration_Project-main/4-MAP/bs_primary_asm.gtf"
rsem_reference_dir = "/home/leomcmahon/06-Integration_Project-main/4-MAP/reference"
output_dir = "/home/leomcmahon/06-Integration_Project-main/4-MAP/rsem_results"

# Log files
output_log = "output.log"
error_log = "error.log"

# Create a log file to store outputs and errors for the entire script
with open(output_log, 'w') as out_f, open(error_log, 'w') as err_f:
    # Step 1: Prepare RSEM reference if not already prepared
    if not os.path.exists(os.path.join(rsem_reference_dir, "reference.grp")):
        print("Preparing RSEM reference...")
        prepare_reference_command = [
            "rsem-prepare-reference",
            "--star",
	    "--star-options", "--genomeSAindexNbases 13",
            "--gtf",
            annotation_gtf,
            cds_fasta,
            os.path.join(rsem_reference_dir, "reference")
        ]
        subprocess.run(prepare_reference_command, check=True, stdout=out_f, stderr=err_f)

    # Step 2: Map reads and calculate expression
    def calculate_expression(fastq_files, sample_name, reference_dir, output_dir):
        stage_name = sample_name.split('_')[0]  # Extract the stage name from the sample name
        stage_output_dir = os.path.join(output_dir, stage_name)  # Create subdirectory for the stage

        # Ensure the output directory exists
        os.makedirs(stage_output_dir, exist_ok=True)

        rsem_output_prefix = os.path.join(stage_output_dir, sample_name)  # Output file prefix with sample name

        rsem_command = [
            "rsem-calculate-expression",
            "--star",
            "--paired-end",
            "-p", "8",
            fastq_files[0],  # Specify the first fastq file
            fastq_files[1],  # Specify the second fastq file
            os.path.join(reference_dir, "reference"),  # Path to reference
            rsem_output_prefix  # Output file prefix
        ]

        # Run RSEM command and log output and errors to the main log files
        subprocess.run(rsem_command, check=True, stdout=out_f, stderr=err_f)

    # Step 3: Traverse directories and select the appropriate fastq files
    def process_fastq_files(base_dir):
        paired_fastq_files = []

        for root, dirs, files in os.walk(base_dir):
            files.sort()

            r1_files = [f for f in files if '_1_paired.fastq' in f or '_1_paired.fq' in f]
            r2_files = [f for f in files if '_2_paired.fastq' in f or '_2_paired.fq' in f]

            stage_name = os.path.basename(root)
            rep_counter = 1  # To add rep1, rep2, etc.

            for r1 in r1_files:
                base_name = r1.replace('_1_paired.fastq', '').replace('_1_paired.fq', '')
                r2 = [f for f in r2_files if base_name in f]

                if r2:
                    r1_full_path = os.path.join(root, r1)
                    r2_full_path = os.path.join(root, r2[0])
                    sample_name = f"{stage_name}_{base_name}_rep{rep_counter}"

                    rep_counter += 1

                    paired_fastq_files.append({
                        'r1': r1_full_path,
                        'r2': r2_full_path,
                        'sample_name': sample_name
                    })

        return paired_fastq_files

    # Step 4: Main workflow
    paired_fastq_files = process_fastq_files(base_dir)

    for pair in paired_fastq_files:
        print(f"Processing sample: {pair['sample_name']}")
        calculate_expression([pair['r1'], pair['r2']], pair['sample_name'], rsem_reference_dir, output_dir)

    print("RSEM quantification complete.")

