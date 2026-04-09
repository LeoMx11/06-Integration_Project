
userID = commandArgs()[1]



setwd(paste0("/home/", userID, "/06-Integration_Project-main/4-MAP/rsem_results"))
library(edgeR)
library(dplyr)

files = list.files()

mapped_data = list()

for (file in files){
      
  vec = base::strsplit(file, split="\\.")[[1]]
  title = vec[1]
  
  if (length(vec) >= 3){
    if (vec[2] == "genes" & vec[3] == "results"){
      
      assign(title, read.table(file))
      mapped_data[length(mapped_data)+1] = title
          
    }
  }
}

for (i in 1:length(mapped_data)){
  write.csv(get(mapped_data[[i]]), paste0("/home/", userID, 
                                          "/06-Integration_Project-main/5-QUANTIFY/output_csvs/", 
                                          mapped_data[[i]]))
}


# Extract gene_id column (first file, V1 without header)
gene_id <- get(mapped_data[[1]])$V1[-1]

# Extract all V5 columns dynamically
mapped_cols <- lapply(mapped_data, function(x) {
  get(x)$V5[-1]
})

# Combine into data frame
mapped_df <- cbind(gene_id, do.call(cbind, mapped_cols))

# Set column names
colnames(mapped_df) <- c("gene_id", mapped_data)



mapped_df = as.data.frame(mapped_df)

mapped_df <- mapped_df %>%
  mutate(across(seq(2,43), as.numeric))

# Save gene IDs
genes <- mapped_df$gene_id

# Remove gene column
counts <- mapped_df[ , -1]

# Convert to matrix
counts <- as.matrix(counts)

# Create DGEList object
dge <- DGEList(counts = counts, genes = genes)

# Calculate TMM normalization factors
dge <- calcNormFactors(dge, method = "TMM")

# View normalization factors
dge$samples

# Adjusting library sizes and converting to counts per million
tmm_counts <- cpm(dge, normalized.lib.sizes = TRUE)

tmm_df <- cbind(genes, tmm_counts)

# write to new csv
write.csv(tmm_df, paste0("/home/", userID, "/06-Integration_Project-main/5-QUANTIFY/final_output.csv"))
