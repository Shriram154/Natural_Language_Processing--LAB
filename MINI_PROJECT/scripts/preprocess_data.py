import os
import json
import pandas as pd
import tfrecord

def process_csv(file_path, output_file, max_records=200):
    count = 0
    df = pd.read_csv(file_path)
    # The project plan stated we only use the 'snippet' field for CSVs.
    if 'snippet' not in df.columns:
        print(f"Warning: 'snippet' column not found in {file_path}")
        return
        
    with open(output_file, 'a', encoding='utf-8') as f:
        for idx, row in df.iterrows():
            if count >= max_records:
                break
            code = str(row['snippet'])
            if code.strip() == "nan" or not code.strip():
                continue
            record = {
                "language": "java",
                "code": code,
                "docstring": ""
            }
            f.write(json.dumps(record) + '\n')
            count += 1
    print(f"Processed {count} records from {file_path}")

def process_tfrecord(file_path, output_file, lang, max_records=200):
    count = 0
    try:
        reader = tfrecord.tfrecord_loader(file_path, None, {
            "code": "byte",
            "docstring": "byte" # Trying common fields; tfrecord format here may vary
        })
        with open(output_file, 'a', encoding='utf-8') as f:
            for record in reader:
                if count >= max_records:
                    break
                # TFRecord formats vary heavily, extracting raw strings if possible
                code_raw = record.get("code", b"")
                doc_raw = record.get("docstring", b"")
                
                # If fields aren't named code/docstring, we will just skip or try 'content'
                if not code_raw:
                    continue
                    
                code_str = code_raw[0].decode('utf-8') if isinstance(code_raw, list) else str(code_raw)
                
                out_rec = {
                    "language": lang,
                    "code": code_str,
                }
                f.write(json.dumps(out_rec) + '\n')
                count += 1
        print(f"Processed {count} records from {file_path}")
    except Exception as e:
        print(f"Error reading TFRecord {file_path}: {e}")

def process_jsonl(file_path, output_file, lang, max_records=200):
    count = 0
    with open(output_file, 'a', encoding='utf-8') as out_f, open(file_path, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            if count >= max_records:
                break
            try:
                data = json.loads(line)
                record = {
                    "language": lang,
                    "code": data.get("code", data.get("original_string", "")),
                    "docstring": data.get("docstring", "")
                }
                if record["code"]:
                    out_f.write(json.dumps(record) + '\n')
                    count += 1
            except Exception as e:
                pass
    print(f"Processed {count} records from {file_path}")

def main():
    base_dir = "datasets"
    out_file = os.path.join(base_dir, "processed", "unified_dataset.jsonl")
    
    # Clear output file if it exists
    if os.path.exists(out_file):
        os.remove(out_file)
        
    print("Starting dataset preprocessing...")
    
    # 1. Archive2 (CSVs)
    archive2_dir = os.path.join(base_dir, "archive2")
    if os.path.exists(archive2_dir):
        for f in os.listdir(archive2_dir):
            if f.endswith(".csv"):
                process_csv(os.path.join(archive2_dir, f), out_file)
                
    # 2. Archive1 (TFRecords)
    archive1_dir = os.path.join(base_dir, "archive1")
    if os.path.exists(archive1_dir):
        for f in os.listdir(archive1_dir):
            if f.endswith(".tfrecord"):
                lang = "java" if "java" in f.lower() else "python"
                process_tfrecord(os.path.join(archive1_dir, f), out_file, lang)
                
    # 3. CodeSearchNet (JSONL)
    csn_dir = os.path.join(base_dir, "codesearchnet")
    if os.path.exists(csn_dir):
        for root, _, files in os.walk(csn_dir):
            for f in files:
                if f.endswith(".jsonl"):
                    lang = "java" if "java" in root.lower() else "python"
                    process_jsonl(os.path.join(root, f), out_file, lang)

    print("Preprocessing completed. Unified dataset saved to datasets/processed/unified_dataset.jsonl")

if __name__ == "__main__":
    main()
