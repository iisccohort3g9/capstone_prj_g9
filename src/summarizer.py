import os
import json
import re
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset
import torch

def load_preprocessed_data(input_dir):
    """
    Load preprocessed JSON data and convert it into a dataset for fine-tuning.
    Each JSON file represents a resume with its summary.
    """
    data = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            with open(os.path.join(input_dir, filename), 'r') as f:
                resume_data = json.load(f)
                # Use the 'summary' field as target and the entire resume text as input
                prompt = (
                    f"Category: {resume_data.get('category', 'General')}\n"
                    f"Resume: {resume_data.get('experience', '')}\n"
                    f"Skills: {resume_data.get('skills', '')}\n"
                    f"Education: {resume_data.get('education', '')}\n"
                    "Generate a concise summary:\n"
                )
                data.append({"input": prompt, "output": resume_data.get("summary", "")})
    return Dataset.from_list(data)

def tokenize_function(examples, tokenizer, max_length=512):
    """
    Tokenize the input and output into a format suitable for GPT fine-tuning.
    """
    inputs = examples["input"]
    targets = examples["output"]
    inputs = [f"{inp} {tokenizer.eos_token}" for inp in inputs]
    targets = [f"{tar} {tokenizer.eos_token}" for tar in targets]
    model_inputs = tokenizer(inputs, max_length=max_length, truncation=True, padding="max_length")
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=max_length, truncation=True, padding="max_length")["input_ids"]
    model_inputs["labels"] = labels
    return model_inputs

def fine_tune_gpt(model_name="gpt2", input_dir="../data/processed_resumes", output_dir="fine_tuned_model"):
    """
    Fine-tune a GPT model using preprocessed resume data.
    """
    # Load data
    print("Loading data...")
    dataset = load_preprocessed_data(input_dir)

    # Load tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Tokenize data
    print("Tokenizing data...")
    tokenized_data = dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True, remove_columns=["input", "output"])

    # Define training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        save_steps=500,
        save_total_limit=2,
        logging_dir="./logs",
        logging_steps=100,
        evaluation_strategy="no",
        learning_rate=5e-5,
        warmup_steps=500,
        weight_decay=0.01,
        fp16=torch.cuda.is_available(),
    )

    # Prepare for training
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # This is causal LM, not masked LM
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_data,
        data_collator=data_collator,
    )

    # Fine-tune the model
    print("Training the model...")
    trainer.train()

    # Save the fine-tuned model
    print(f"Saving the fine-tuned model to {output_dir}...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

if __name__ == "__main__":
    # Fine-tune GPT-2 on preprocessed resume data
    fine_tune_gpt()
