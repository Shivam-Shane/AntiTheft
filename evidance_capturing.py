import cv2
import pyaudio
import wave
import os
from datetime import datetime
import threading
from logger import logging

# Function to capture an image from the webcam
def capture_image(output_dir="captures"):
    """
    Captures an image from the webcam and saves it to the specified directory.
    Args: (output_dir) The directory where the image will be saved
    Returns: None
    """
    os.makedirs(output_dir, exist_ok=True)

    # Open the webcam (camera index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        logging.error("Error: Could not open the camera.")
        return

    # Capture the image
    ret, frame = cap.read()
    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(output_dir, f"image_{timestamp}.jpg")
        cv2.imwrite(file_path, frame)
        logging.info(f"Image captured and saved to {file_path}")
    else:
        logging.error("Error: Could not read frame, while capturing the image.")

    # Release the camera
    cap.release()

# Function to record audio
def record_audio(duration=10, output_dir="captures"):
    """
    Records audio for the specified duration (in seconds).
    Args: (duration) The duration (in seconds) of the audio
         (output_dir) The directory where the audio will be saved
    returns: None
    """
    os.makedirs(output_dir, exist_ok=True)

    # Set up PyAudio
    p = pyaudio.PyAudio()

    # Open an audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    frames = []

    logging.info(f"Recording audio for {duration} seconds...")

    for _ in range(0, int(44100 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    logging.info("Audio recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the audio to a file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_file = os.path.join(output_dir, f"audio_{timestamp}.wav")
    wf = wave.open(audio_file, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
    logging.info(f"Audio recorded and saved to {output_dir}")

# Function to record a video
def record_video(duration=10, output_dir="captures"):
    """
    Records a video for the specified duration (in seconds).
    Args: (duration) The duration (in seconds) of the video
    (output_dir) The directory where the video will be saved
    Returns: None
    """
    os.makedirs(output_dir, exist_ok=True)

    # Open the default camera (camera index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        logging.error("Error: Could not open the camera.")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS) or 30)  # Fallback to 30 FPS if unavailable

    # Video writer for saving the recording
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"video_{timestamp}.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(file_path, fourcc, fps, (frame_width, frame_height))

    logging.info(f"Recording video for {duration} seconds...")

    # Record video for the specified duration
    start_time = datetime.now()
    while (datetime.now() - start_time).seconds < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            logging.error("Error: Could not read frame.")
            break

    # Release resources
    cap.release()
    out.release()
    logging.info(f"Video recorded and saved to {file_path}")

# Function to capture evidence
def capture_evidence():
    """
    Capture evidence
    Captures images and audio/video simultaneously in separate threads
    Args: None
    Returns: None
    """
    # Capture image
    capture_image()

    # Record video and audio in parallel using threads
    video_thread = threading.Thread(target=record_video, args=(10,))
    audio_thread = threading.Thread(target=record_audio, args=(10,))

    video_thread.start()
    audio_thread.start()

    video_thread.join()
    audio_thread.join()

    # Get the file paths of the video and audio (these are dynamically generated)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # os.path.join("captures", f"video_{timestamp}.avi")
    os.path.join("captures", f"audio_{timestamp}.wav")