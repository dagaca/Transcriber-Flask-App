import os
import moviepy.editor as mpe
import speech_recognition as spr
from flask import current_app

def is_valid_file(file_name):
    """
    Check if the file has an allowed extension.

    Args:
        file_name (str): The name of the file.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    valid_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in valid_extensions

def convert_video_to_audio(clip, start, end, output):
    """
    Extract audio from a video clip between start and end time.

    Args:
        clip (VideoFileClip): The video clip object.
        start (float): Start time in seconds.
        end (float): End time in seconds.
        output (str): Path to save the extracted audio file.
    """
    audio_part = clip.subclip(start, end).audio
    audio_part.write_audiofile(output)

def get_text_from_audio(audio_file_path, lang='en'):
    """
    Extract text from an audio file using speech recognition.

    Args:
        audio_file_path (str): Path to the audio file.
        lang (str): Language code for speech recognition.

    Returns:
        str: Recognized text from the audio.
    """
    recognizer = spr.Recognizer()
    with spr.AudioFile(audio_file_path) as source:
        audio_content = recognizer.record(source)
        try:
            recognized_text = recognizer.recognize_google(audio_content, language=lang)
        except spr.UnknownValueError:
            recognized_text = "[Error: Could not understand the audio]"
        except spr.RequestError:
            recognized_text = "[Error: Could not request results from Google Speech Recognition service]"
    return recognized_text

def process_media_file(file_path, lang):
    """
    Convert video to audio and extract text from each segment.

    Args:
        file_path (str): Path to the video file.
        lang (str): Language code for speech recognition.

    Returns:
        str: Concatenated recognized text from the video.
    """
    temp_dir = current_app.config['UPLOAD_FOLDER']
    full_text = ""
    file_name = os.path.basename(file_path)
    video_clip = mpe.VideoFileClip(file_path)
    total_time = video_clip.duration
    part_duration = 180
    num_parts = int(total_time / part_duration)

    temp_path = os.path.join(os.getcwd(), temp_dir)
    segment_dir_path = os.path.join(temp_path, os.path.splitext(file_name)[0])
    os.makedirs(segment_dir_path, exist_ok=True)
    
    for i in range(num_parts):
        start_time = i * part_duration
        end_time = min((i + 1) * part_duration, total_time)
        output_path = os.path.join(segment_dir_path, f"segment_{start_time}_{end_time}.wav")
        convert_video_to_audio(video_clip, start_time, end_time, output_path)
        segment_text = get_text_from_audio(output_path, lang)
        full_text += segment_text + " "
        os.remove(output_path)

    if total_time % part_duration != 0:
        start_time = num_parts * part_duration
        end_time = total_time
        output_path = os.path.join(segment_dir_path, f"segment_{start_time}_{end_time}.wav")
        convert_video_to_audio(video_clip, start_time, end_time, output_path)
        segment_text = get_text_from_audio(output_path, lang)
        full_text += segment_text
        os.remove(output_path)

    video_clip.close()
    return full_text