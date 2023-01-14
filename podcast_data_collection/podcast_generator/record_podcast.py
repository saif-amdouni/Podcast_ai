import os
from TTS.api import TTS

class PodcastRecorder:
    def __init__(self):
        self.engine = TTS(model_name='tts_models/en/ek1/tacotron2', progress_bar=True, gpu=False)
        self.podcast_folder= "podcast_data_collection/Data/Data_03/Health_Data"
    
    def read_files(self):
        for filename in os.listdir(self.podcast_folder):
            if filename.endswith(".txt"):
                self.read_podcast(os.path.join(self.podcast_folder, filename))
                
    def read_podcast(self, file_path):
        """Read the given podcast text using TTS"""
        with open(file_path, "r") as file:
            content = file.read()
            try:
                # Run TTS
                self.engine.tts_to_file(text=content, file_path=os.path.join(os.path.dirname(file_path),"podcast.wav"))
                print(f"Successfully generated TTS for {file_path}")
            except Exception as e:
                print(f"Error generating TTS for {file_path}: {e}")
        
    def save_audio(self, podcast_text, file_name):
        """Save the audio of the TTS reading of the podcast to a file"""
        self.engine.save_to_file(podcast_text, file_name)
        self.engine.runAndWait()
        
    def change_voice(self, voice_id):
        """Change the voice used for TTS"""
        self.engine.setProperty('voice', voice_id)
        
    def read_and_save_podcast(self, podcast_text, file_name):
        """Read the given podcast text using TTS and save the audio to a file"""
        
        self.read_podcast(podcast_text)
        self.save_audio(podcast_text, file_name)
        
if __name__ == "__main__":
    PodcastRec= PodcastRecorder()
    PodcastRec.read_files()
    