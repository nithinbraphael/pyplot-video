import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path
from frameGeneration import extract_frames

def play_video(video_path):
    frames_dir, fps = extract_frames(video_path)
    frame_paths = sorted(frames_dir.glob("frame_*.png"))
    if not frame_paths:
        raise ValueError("No frames were extracted.")

    first_frame = mpimg.imread(frame_paths[0])
    fig, ax = plt.subplots()
    image_display = ax.imshow(first_frame)
    ax.axis("off")
    plt.tight_layout()

    try:
        for frame_path in frame_paths[1:]:
            if not plt.fignum_exists(fig.number):
                break
            frame = mpimg.imread(frame_path)
            image_display.set_data(frame)
            fig.canvas.draw_idle()
            plt.pause(1 / fps)
    finally:
        if plt.fignum_exists(fig.number):
            plt.close(fig)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        video_path = input("Enter the path to the video: ").strip()
    else:
        video_path = " ".join(sys.argv[1:]).strip()
    try:
        play_video(video_path)
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"Error: {error}")
