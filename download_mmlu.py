from datasets import load_dataset
import os

# The folder where we are saving the files
save_folder = "/Users/faizhussain/Desktop/thesis_project"

print("Downloading MMLU dataset from Hugging Face...")
print("(This is a large dataset, so it might take a minute or two!)")

# Load the "all" subset of the MMLU dataset
mmlu_dataset = load_dataset("cais/mmlu", "all")

# Define exactly where each CSV file will be saved
test_file = os.path.join(save_folder, "mmlu_test.csv")
validation_file = os.path.join(save_folder, "mmlu_validation.csv")
dev_file = os.path.join(save_folder, "mmlu_dev.csv")
train_file = os.path.join(save_folder, "mmlu_auxiliary_train.csv")

print(f"\nConverting data and saving files to: {save_folder}")

# Convert and save each split
mmlu_dataset["test"].to_csv(test_file)
print("✅ Saved mmlu_test.csv (14k rows)")

mmlu_dataset["validation"].to_csv(validation_file)
print("✅ Saved mmlu_validation.csv (1.53k rows)")

mmlu_dataset["dev"].to_csv(dev_file)
print("✅ Saved mmlu_dev.csv (285 rows)")

mmlu_dataset["auxiliary_train"].to_csv(train_file)
print("✅ Saved mmlu_auxiliary_train.csv (99.8k rows)")

