import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import json
import os

def analyze_audio(file_path):
    print(f"--- Starting Forensic Analysis on: {file_path} ---")
    
    try:
        # 1. Load the audio (Target 22050Hz for standard forensic mapping)
        y, sr = librosa.load(file_path, sr=22050)

        # 2. Compute Mel-scaled power spectrogram
        # This turns raw sound waves into frequency data
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)

        # 3. Convert to log scale (decibels)
        # This is the 'human' way of seeing sound levels
        S_dB = librosa.power_to_db(S, ref=np.max)

        # 4. Generate the Physical Result: PNG Spectrogram
        plt.figure(figsize=(12, 6))
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title(f"Forensic Frequency Map: {os.path.basename(file_path)}")
        plt.tight_layout()
        
        # Saving directly to the root so GitHub Actions can see it
        plt.savefig("analysis_map.png")
        plt.close()
        print("Successfully created: analysis_map.png")

        # 5. Generate the Physical Result: JSON Data
        # We take the mean power across time for 128 frequency bands
        spectral_data = np.mean(S_dB, axis=1).tolist()
        
        output_data = {
            "filename": os.path.basename(file_path),
            "duration_seconds": float(librosa.get_duration(y=y, sr=sr)),
            "frequency_map": spectral_data
        }

        with open("analysis_data.json", "w") as f:
            json.dump(output_data, f)
        print("Successfully created: analysis_data.json")

    except Exception as e:
        print(f"ERROR: Could not process file. {e}")

if __name__ == "__main__":
    # This logic automatically finds the first .wav file in your 'uploads' folder
    upload_folder = "uploads"
    
    if os.path.exists(upload_folder):
        files = [f for f in os.listdir(upload_folder) if f.endswith(('.wav', '.mp3', '.m4a'))]
        if files:
            target_file = os.path.join(upload_folder, files[0])
            analyze_audio(target_file)
        else:
            print("No audio files found in 'uploads/'. Drop a .wav file there.")
    else:
        print("Folder 'uploads/' not found. Please create it.")
