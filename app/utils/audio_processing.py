import os
import moviepy.editor as mp
import speech_recognition as sr
from flask import current_app

def allowed_file(filename):
    """
    Check if the file has an allowed extension.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def video_to_audio(video_clip, start_time, end_time, output_path):
    """
    Extract audio from a video clip between start_time and end_time.

    Args:
        video_clip (VideoFileClip): The video clip object.
        start_time (float): Start time in seconds.
        end_time (float): End time in seconds.
        output_path (str): Path to save the extracted audio file.
    """
    audio_segment = video_clip.subclip(start_time, end_time).audio
    audio_segment.write_audiofile(output_path)

def extract_text_from_audio(audio_path, language='en'):
    """
    Extract text from an audio file using speech recognition.

    Args:
        audio_path (str): Path to the audio file.
        language (str): Language code for speech recognition.

    Returns:
        str: Recognized text from the audio.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language=language)
        except sr.UnknownValueError:
            text = "[Error: Could not understand the audio]"
        except sr.RequestError:
            text = "[Error: Could not request results from Google Speech Recognition service]"
    return text

def process_video(video_path, language):
    """
    Convert video to audio and extract text from each segment.

    Args:
        video_path (str): Path to the video file.
        language (str): Language code for speech recognition.

    Returns:
        str: Concatenated recognized text from the video.
    """
    temp_folder = current_app.config['UPLOAD_FOLDER']
    recognized_text = ""
    video_filename = os.path.basename(video_path)
    video_clip = mp.VideoFileClip(video_path)
    total_duration = video_clip.duration
    segment_duration = 180
    num_segments = int(total_duration / segment_duration)

    temp_folder_path = os.path.join(os.getcwd(), temp_folder)
    file_subfolder_path = os.path.join(temp_folder_path, os.path.splitext(video_filename)[0])
    os.makedirs(file_subfolder_path, exist_ok=True)
    
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, total_duration)
        output_path = os.path.join(file_subfolder_path, f"segment_{start_time}_{end_time}.wav")
        video_to_audio(video_clip, start_time, end_time, output_path)
        text = extract_text_from_audio(output_path, language)
        recognized_text += text + " "
        os.remove(output_path)

    if total_duration % segment_duration != 0:
        start_time = num_segments * segment_duration
        end_time = total_duration
        output_path = os.path.join(file_subfolder_path, f"segment_{start_time}_{end_time}.wav")
        video_to_audio(video_clip, start_time, end_time, output_path)
        text = extract_text_from_audio(output_path, language)
        recognized_text += text
        os.remove(output_path)

    video_clip.close()
    return recognized_text