import os
import sys
import subprocess

userID = sys.argv[1]

# Set paths
base_dir = f"/home/{userID}/06-Integration_Project-main/0-DATA/FASTQ_files"
output_dir = f"/home/{userID}/06-Integration_Project-main/3-TRIM"
adapters_path = f"/home/{userID}/06-Integration_Project-main/3-TRIM/Trimmomatic/TruSeq3-PE.fa"  # Updated adapter path
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
def process_fastq(base_dir):
    print(os.listdir(base_dir))  # Debugging: list files in the directory
    fastq_files = sorted([f for f in os.listdir(base_dir) if f.endswith((".fastq", ".fastq.gz", ".fq"))])
    if not fastq_files:
        print(f"No FASTQ files found in {base_dir}")
        return  # Skip if no FASTQ files found

    for i in range(0, len(fastq_files), 2):  # Assuming paired files are grouped together
        try:
            forward_read = os.path.join(fastq_files[i])
            reverse_read = os.path.join(fastq_files[i + 1])
            sample_id = os.path.basename(fastq_files[i])[:-8]

            # Output files in the stage's subdirectory
            output_forward_paired = os.path.join(processed_dir, f"{sample_id}_1_paired.fastq")
            output_forward_unpaired = os.path.join(processed_dir, f"{sample_id}_1_unpaired.fastq")
            output_reverse_paired = os.path.join(processed_dir, f"{sample_id}_2_paired.fastq")
            output_reverse_unpaired = os.path.join(processed_dir, f"{sample_id}_2_unpaired.fastq")

            # Trimmomatic command
            cmd = [
                "trimmomatic", "PE",
                "-threads", str(threads), "-phred33", # phred33 manually encodes the correct reading for newer datasets
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
            print(f"Unpaired file detected: {fastq_files[i:]}")
            return  # Skip unpaired files


process_fastq(base_dir)

print("Trimmomatic complete. Logs are in 'error_trimmomatic.log' and 'out_trimmomatic.log'.")
