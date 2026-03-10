import os
import subprocess

# Set paths
base_dir = "/home/leomcmahon/06-Integration_Project/0-DATA/FASTQ_files"
output_dir = "/home/leomcmahon/06-Integration_Project/3-TRIM"
adapters_path = "/home/leomcmahon/06-Integration_Project/3-TRIM/Trimmomatic/TruSeq3-PE.fa"  # Updated adapter path
threads = 8  # Number of threads to use for Trimmomatic

# Create processed_FASTQ directory
processed_dir = os.path.join(output_dir, "processed_FASTQ")
os.makedirs(processed_dir, exist_ok=True)

# Define shared log files
error_log = os.path.join(output_dir, "error_trimmomatic.log")
output_log = os.path.join(output_dir, "out_trimmomatic.log")

# Clear previous logs if they exist
open(error_log, "w").close()
open(output_log, "w").close()

# Function to process FASTQ files in a directory
def process_fastq(stage_dir, stage_name):
    print(f"Listing contents of {stage_dir}:")
    print(os.listdir(stage_dir))  # Debugging: list files in the directory
    fastq_files = sorted([f for f in os.listdir(stage_dir) if f.endswith((".fastq", ".fastq.gz", ".fq"))])
    if not fastq_files:
        print(f"No FASTQ files found in {stage_dir}")
        return  # Skip if no FASTQ files found
    
    # Create a subdirectory for the current stage
    stage_output_dir = os.path.join(processed_dir, stage_name)
    os.makedirs(stage_output_dir, exist_ok=True)

    for i in range(0, len(fastq_files), 2):  # Assuming paired files are grouped together
        try:
            forward_read = os.path.join(stage_dir, fastq_files[i])
            reverse_read = os.path.join(stage_dir, fastq_files[i + 1])
            sample_id = os.path.basename(fastq_files[i]).rsplit("_", 1)[0]

            # Output files in the stage's subdirectory
            output_forward_paired = os.path.join(stage_output_dir, f"{sample_id}_1_paired.fastq")
            output_forward_unpaired = os.path.join(stage_output_dir, f"{sample_id}_1_unpaired.fastq")
            output_reverse_paired = os.path.join(stage_output_dir, f"{sample_id}_2_paired.fastq")
            output_reverse_unpaired = os.path.join(stage_output_dir, f"{sample_id}_2_unpaired.fastq")

            # Trimmomatic command
            cmd = [
                "trimmomatic", "PE",
                "-threads", str(threads),
                forward_read, reverse_read,
                output_forward_paired, output_forward_unpaired,
                output_reverse_paired, output_reverse_unpaired,
                f"ILLUMINACLIP:{adapters_path}:2:30:10",
                "LEADING:3", "TRAILING:3", "SLIDINGWINDOW:4:20", "MINLEN:36"
            ]
            print(f"Processing sample: {sample_id}")
            print(f"Command: {' '.join(cmd)}")

            # Run command and append logs
            with open(output_log, "a") as log, open(error_log, "a") as error:
                subprocess.run(cmd, stdout=log, stderr=error)
        except IndexError:
            print(f"Unpaired file detected in {stage_dir}: {fastq_files[i:]}")
            return  # Skip unpaired files

# Traverse each subdirectory and process FASTQ files
for stage_dir in os.listdir(base_dir):
    stage_path = os.path.join(base_dir, stage_dir)
    if os.path.isdir(stage_path):
        print(f"Processing stage directory: {stage_path}")
        process_fastq(stage_path, stage_dir)

print("Processing complete. Logs are in 'error_trimmomatic.log' and 'out_trimmomatic.log'.")
