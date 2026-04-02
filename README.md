
# Integrating Bulk RNA-seq Data to Genome Pipeline

***By Leo McMahon***

This pipeline outlines how to go from raw bulk RNA-seq reads, in this case drawn from the NCBI Sequence Read Archive (SRA) using the SRA Toolkit.

In using this pipeline, different projects will have to start at different steps. For example, if you already have your .fastq files ready from another source other than SRA, you can obviously skip the first step of downloading the .fastq files from NCBI.

Additionally, in using the MASTERPROCESS file, all of the necessary steps (starting when .fastq files have already been collected) will be executed sequentially with no outside input from the user. However, if you only want to use one of the steps, the individual files will also be included so that a step-by-step process can be used if necessary.

## Step 0: Clone this repository to Pod

You can do this any way you know how, but the most beginner-friendly way is as follows:

In the home page of this repository, click the blue Code icon and then press Download Zip at the bottom of the menu.

Then find the pathname for this file (on Mac I search for it in the Finder app and then Ctrl+Click and select "Copy file as Pathname"). Then it is in your clipboard.

Then we will transfer the zip file to our pod account using `scp` in a Terminal Window:

```bash
scp /path/to/06-Integration_Project-main.zip yourUCSBnetID@pod-login1.cnsi.ucsb.edu:/home/yourUCSBnetID/
```

So for me this was:

```bash
scp /Users/leomcmahon/Downloads/06-Integration_Project-main.zip leomcmahon@pod-login1.cnsi.ucsb.edu:/home/leomcmahon/
```

Now that the zip file is in your Pod, simply go to your Pod's home page and perform:

```bash
unzip 06-Integration_Project-main.zip
```

## Step 1: Collect your data

If you already have your .fastq files, skip this step. But if you are accessing your files from the NCBI SRA, follow this step.

The general steps for downloading and utilizing the SRA toolkit are here: https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit.

For my fellow UCSB Pod users however, I will outline exactly what I did on my computer to get this to work on the Pod.

### Download SRA Toolkit to Personal Computer

First, click on the link above to reach the SRA Toolkit Github page and navigate to step: 02. Installing SRA Toolkit.

At the top there should be a box with each OS' own SRA Toolkit binaries. Click on the AlmaLinux link to download that into your computer.

Now you will need to find the pathname of your newly downloaded file. On a Mac, I use the Finder App to search for sratoolkit and then Ctrl+Click on the file and select "Copy file as Pathname". Then it is copied to your clipboard.

### Transfer SRA Toolkit .zip file to Pod account

Now open *a new terminal window* (if you have a pod window open, don't close it, just press and hold the Terminal icon on your screen until the New Window option appears, then click that).

In this new window, you will use the `scp` function to transfer this file onto your pod account. The general format of this function is as follows:

```bash
scp /copy_of_the_filename_from_previous_step/sratoolkit.current-alma_linux64.tar.gz yourUCSBnetID@pod-login1.cnsi.ucsb.edu:/home/yourUCSBnetID/06-Integration_Project-main/1-SRA_Toolkit
```

So for me this was:

```bash
scp /Users/leomcmahon/000-LabStuff/06-Integration_Project/1-SRA_Toolkit/sratoolkit.current-alma_linux64.tar.gz leomcmahon@pod-login1.cnsi.ucsb.edu:/home/leomcmahon/06-Integration_Project-main/1-SRA_Toolkit
```

You will have to enter the password to your pod account to complete the transfer.

### Unzip SRA Toolkit

Now that the zip file is in your Pod directory, log into your Pod account and enter the SRA Toolkit directory:

```bash
cd 06-Integration_Project-main/1-SRA_Toolkit/
```

Check that this works by running the `ls` command. You should have `SRA_placeholder.md` file and your downloaded zip file.

Now run the following to unzip the SRA Toolkit:

```bash
tar -vxzf sratoolkit.current-alma_linux64.tar.gz
```

Then append the path to the binaries to your PATH environment variable (fill in the X's with the version that was downloaded; if you need to check this, run `ls` and see what numbers are in the name of the new unzipped directory)

```bash
export PATH=$PWD/sratoolkit.3.X.X-alma_linux64/bin:$PATH
```

Now, run the following to check for success:

```bash
which fastq-dump
```

This should point somewhere in your SRA Toolkit directory. If that works, you will have everything you need to download SRA files into your pod account.

### Finding correct SRA code

Now that you have all of the programs necessary, you need to find where your data is stored in the SRA. This may take some digging, but if your data comes from a paper, there should be some link to the sequences in the related links or data section. I will show where I found mine.

In my paper of focus (https://pubmed.ncbi.nlm.nih.gov/25542255/) there is a link entitled SRA in the related links section:

![](image here)

Clicking this brings me to a list of all of the samples from this paper. If I wanted to download only a particular one or few, I could click on them and find their individual codes for prefetching. For mine, after clicking on an individual link, the run code is what I used to set up the download.

![](image here)

However, I want to download all of these. The way I was able to do that is by finding a code that encompasses all of my samples. For my data, the easiest way to find it was by clicking on one sample, then under the Study heading, there is a code that begins with SR (mine was SRP048687) 

![](image here)

### Downloading the data into Pod

Now that you have your code for the larger dataset (or if you are just doing a few individual runs, use each code individually), we will run the following code usign your codes:

```bash
prefetch SRP048687
```

Since this one code contains 42 different samples of millions of bases, this might take a while to run, so take a well-earned break while that downloads in the background. 

Once that is done, you will need to actually extract fastq files from this location. For this, I recommend running this code (assuming your codes are SRR's):

```bash
for srr in SRR*; do
    fasterq-dump "$srr" --outdir ~/06-Integration_Project-main/0-DATA/FASTQ_files
done
```

Now you have all of the necessary fastq files in your Pod!

## Step 1.5: Rename your data (optional but recommended)

At this point, you could move on to step 2 and run MASTERPROCES now, but when the program is finished running your R dataframe's column names will be basically just what the fastq file names are. Thus if you leave it as SRR4829023, there's not much information about the sample. So at this point I like to leave some sort of signifier as to what the sample is. In my example dataset, the samples are described by their fertility, the name of the colony they came from, and the stage they came from. If you want to use my graphing program later on to graph your data, you should separate all of this information by underscores for each sample. 

How to do this is simple; we use the `mv` function to rename the datasets to what we need. As described above, here is an example of how I renamed one of my samples:

```bash
mv SRR1604821_1.fastq F_801_A1_1.fastq
mv SRR1604821_2.fastq F_801_A1_2.fastq
```

Be careful to keep both strands (this is the 1 and 2 at the end of the names) consistent with all else being identical except the strand names.

Once your fastq files are all named as you want your column names at the end, you are ready for the next step.

## Step 2: MASTERPROCESS








