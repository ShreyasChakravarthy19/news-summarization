"""import os
import time
from gtts import gTTS

class TextToSpeechService:
    def __init__(self):
        self.static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        os.makedirs(self.static_folder, exist_ok=True)

    def convert_text_to_speech(self, text):
        tts = gTTS(text=text, lang='en')
        # Generate unique filename using timestamp
        filename = f'output_{int(time.time())}.mp3'
        # Full path in static folder
        filepath = os.path.join(self.static_folder, filename)
        # Save the file
        tts.save(filepath)
        return filename"""


import os
import time
from gtts import gTTS

class TextToSpeechService:
    def __init__(self):
        self.static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        os.makedirs(self.static_folder, exist_ok=True)

    def convert_text_to_speech(self, text):
        """
        Convert the given text to speech and save it as an MP3 file.
        Handles long text by splitting it into chunks if necessary.
        """
        try:
            # Ensure text is not empty
            if not text.strip():
                raise ValueError("Text for TTS cannot be empty.")

            # Generate unique filename using timestamp
            filename = f'output_{int(time.time())}.mp3'
            filepath = os.path.join(self.static_folder, filename)

            # Check if text exceeds gTTS limit (around 200 characters per chunk)
            if len(text) > 200:
                # Split text into smaller chunks
                chunks = self._split_text_into_chunks(text, max_length=200)
                # Combine audio chunks
                self._combine_audio_chunks(chunks, filepath)
            else:
                # Convert text directly to speech
                tts = gTTS(text=text, lang='en')
                tts.save(filepath)

            return filename  # Return the filename for use in templates
        except Exception as e:
            print(f"Error in TextToSpeechService: {e}")
            return None

    def _split_text_into_chunks(self, text, max_length=200):
        """
        Split text into smaller chunks of a specified maximum length.
        """
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            # Check if adding the word exceeds the max length
            if len(" ".join(current_chunk + [word])) > max_length:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
            else:
                current_chunk.append(word)

        # Add the last chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def _combine_audio_chunks(self, chunks, output_filepath):
        """
        Combine multiple audio chunks into a single MP3 file.
        """
        from pydub import AudioSegment
        from pydub.playback import play

        combined_audio = None

        for chunk in chunks:
            tts = gTTS(text=chunk, lang='en')
            temp_filepath = os.path.join(self.static_folder, f'temp_{int(time.time())}.mp3')
            tts.save(temp_filepath)

            # Load the audio chunk
            audio_chunk = AudioSegment.from_file(temp_filepath)

            # Combine with the previous audio
            if combined_audio is None:
                combined_audio = audio_chunk
            else:
                combined_audio += audio_chunk

            # Remove the temporary file
            os.remove(temp_filepath)

        # Export the combined audio to the output file
        if combined_audio:
            combined_audio.export(output_filepath, format="mp3")