import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import json
import os

def analyze_audio(file_path):
    # 1. Get the original name (e.g., "Brenda's Got A Baby")
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # 2. CLEAN THE NAME: Remove spaces and apostrophes for the "Manager"
    # This turns "Brenda's Got A Baby" into "Brendas_Got_A_Baby"
    clean_name = base_name.replace(" ", "_").replace("'", "").replace("-", "_")
    
    print(f"--- Auditing: {clean_name} ---")
    
    y, sr = librosa.load(file_path, sr=22050)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)

    # 3. Save the Physical Map with the CLEAN name
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    
    # This is the line that creates the file the YAML is looking for
    plt.savefig(f"map_{clean_name}.png") 
    plt.close()

    # 4. Save the Physical JSON with the CLEAN name
    spectral_data = np.mean(S_dB, axis=1).tolist()
    with open(f"data_{clean_name}.json", "w") as f:
        json.dump({"track": clean_name, "frequencies": spectral_data}, f)
    
    print("Success: Physical results created in root directory.")

import shutil # Add this at the very top of your file

if __name__ == "__main__":
    upload_folder = "uploads"
    processed_folder = "processed"
    
    # Create the 'archive' if it doesn't exist
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    if os.path.exists(upload_folder):
        audio_files = [f for f in os.listdir(upload_folder) if f.endswith(('.wav', '.mp3'))]
        
        for filename in audio_files:
            full_path = os.path.join(upload_folder, filename)
            
            # 1. RUN THE MATH
            analyze_audio(full_path)
            
            # 2. MOVE THE EVIDENCE (The Janitor step)
            # This prevents the script from re-running this file next time
            shutil.move(full_path, os.path.join(processed_folder, filename))
            print(f"Moved {filename} to processed folder.")
    else:
        print("No uploads found.")

