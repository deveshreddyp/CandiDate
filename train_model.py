import csv
import os
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# 1. Load the Generic Brain (Pre-trained)
print("Loading generic model 'all-MiniLM-L6-v2'...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Prepare the Training Data
train_examples = []

def load_data_from_csv(filepath, source_name):
    if not os.path.exists(filepath):
        print(f"⚠️ Skipping {source_name}: File not found ({filepath})")
        return 0
    
    print(f"Reading {source_name}...")
    count = 0
    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Convert 0-100 score to 0.0-1.0 format for the model
                float_score = float(row['human_score']) / 100.0
                # Create a training example: [Resume, JD] -> Score
                example = InputExample(texts=[row['resume_text'], row['jd_text']], label=float_score)
                train_examples.append(example)
                count += 1
            except ValueError:
                continue
    print(f"✅ Loaded {count} samples from {source_name}")
    return count

# Load Base Data (Synthetic)
count_synthetic = load_data_from_csv('synthetic_dataset.csv', "Synthetic Data")

# Load Real Data (User Feedback)
count_feedback = load_data_from_csv('training_data.csv', "User Feedback")

total_samples = count_synthetic + count_feedback

if total_samples == 0:
    print("❌ Error: No training data found in either file. Please run generate_data.py first.")
    exit()

# 3. Create a Data Loader (Batching)
# We use a small batch size (8) to ensure it runs on any laptop CPU
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=8)

# 4. Define the Loss Function (Cosine Similarity Loss)
# This mathematically forces the vector angle to match your score
train_loss = losses.CosineSimilarityLoss(model)

# 5. Train the Model (Fine-Tuning)
print(f"\nStarting Training with {total_samples} total samples...")
print("This process will take about 1-3 minutes depending on your CPU.")

model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=3,  # Iterate through the data 3 times
    warmup_steps=10,
    output_path='./fine_tuned_model' # Save the new brain to this folder
)

print("\nSUCCESS! Training Complete.")
print("New model saved in 'backend/fine_tuned_model'")