import cv2
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from nltk.tokenize import sent_tokenize

#function to process the video and perform segmentation
def segment_video(video_path, output_path):
    #step 1: Load the video
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    
    #step 2: Extract audio from the video
    clip = VideoFileClip(video_path)
    audio = clip.audio
    audio_file = "extracted_audio.wav"
    audio.write_audiofile(audio_file)
    
    #step 3: Transcribe audio
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    
    #step 4: Text Segmentation
    sentences = sent_tokenize(text)
    segment_boundaries = []
    for i, sentence in enumerate(sentences):
        if "move the mouse" in sentence or "click a button" in sentence:
            time = i  #somehow calculate the time based on the sentence's position in the audio.
            segment_boundaries.append(time)
    
    #dtep 5: Map segments to video
    segments = []
    start_time = 0
    for boundary in segment_boundaries:
        #calculate the frame number based on the time and FPS
        frame_number = boundary * fps
        #use the frame number to segment the video
        end_time = boundary
        segments.append((start_time, end_time))
        start_time = end_time
    
    #step 6: Output segmented video
    for i, (start, end) in enumerate(segments):
        #extract segment and save to output path
        #clipping the video using moviepy with start and end times and writing it to a file.
        output_filename = f"{output_path}/segment_{i}.mp4"
    
    return segments
