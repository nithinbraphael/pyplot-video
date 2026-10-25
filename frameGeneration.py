import cv2
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
FRAMES_DIR = PROJECT_DIR/"data"/"frames"

def extract_frames(video_path):
    video_path = Path(video_path).expanduser().resolve()
    if not video_path.is_file():
        raise FileNotFoundError(f"Video not found: {video_path}")

    video_name = video_path.stem
    output_dir = FRAMES_DIR/video_name
    output_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        cap.release()
        raise ValueError("Could not determine the video's frame rate.")

    frame_count = 0

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break
            frame_path = output_dir / f"frame_{frame_count:06d}.png"
            if not cv2.imwrite(str(frame_path), frame):
                raise OSError(f"Could not save frame: {frame_path}")
            frame_count += 1
    finally:
        cap.release()

    print(f"Extracted {frame_count} frames.")
    print(f"Saved to: {output_dir}")
    print(f"Original FPS: {fps:.2f}")
    return output_dir, fps
