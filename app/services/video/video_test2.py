from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from datetime import datetime
import os

from app.utils.s3_tempfile import download_s3_to_tempfile, cleanup_tempfiles

async def create_pose_video(
    db,
    pose_ids: list,
    music_id: str,
    guide_labels: list
):
    pose_img_url1 = "s3://yot-static-files/pose/Child's Pose.png"
    pose_img_url2 = "s3://yot-static-files/pose/Eagle.png"
    bg_music_url = "s3://yot-static-files/background_music/rain_1.mp3"

    pose_img_path1 = download_s3_to_tempfile(pose_img_url1)
    pose_img_path2 = download_s3_to_tempfile(pose_img_url2)
    bg_audio_path = download_s3_to_tempfile(bg_music_url)

    temp_files = [pose_img_path1, pose_img_path2, bg_audio_path]

    # 기준 해상도 지정 (예: 첫 번째 이미지 크기)
    base_clip = ImageClip(pose_img_path1, duration=10)
    w, h = base_clip.size

    # 두 이미지 모두 같은 해상도로 맞춤
    pose_img1 = base_clip
    pose_img2 = ImageClip(pose_img_path2, duration=10).resized((w, h))

    # 오디오 준비
    try:
        bg_audio = AudioFileClip(bg_audio_path).subclipped(0, 20)
    except Exception as e:
        cleanup_tempfiles(temp_files)
        raise RuntimeError("오디오 파일에 문제가 있습니다.")

    # 이어붙이기
    video_clip = concatenate_videoclips([pose_img1, pose_img2])
    video_clip.audio = bg_audio

    output_dir = "generated_videos"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"test_video_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
    output_path = os.path.join(output_dir, filename)

    video_clip.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    cleanup_tempfiles(temp_files)
    return output_path
