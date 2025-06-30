from moviepy.editor import ImageClip, AudioFileClip
from datetime import datetime
import os

from app.utils.s3_tempfile import download_s3_to_tempfile, cleanup_tempfiles

async def create_pose_video(
    db,
    pose_ids: list,
    music_id: str,
    guide_labels: list
):
    # 테스트용 S3 경로 (실제 파일 경로로 교체)
    pose_img_url = "s3://yot-static-files/pose/Eagle.png"
    bg_music_url = "s3://yot-static-files/background_music/rain_1.mp3"

    # S3에서 파일 다운로드
    pose_img_path = download_s3_to_tempfile(pose_img_url)
    bg_audio_path = download_s3_to_tempfile(bg_music_url)

    # 오디오 클립 생성 및 10초로 자르기
    bg_audio = AudioFileClip(bg_audio_path).subclip(0, 10)

    # 이미지 클립 생성, 오디오 길이에 맞춰 duration 지정
    pose_img = ImageClip(pose_img_path).set_duration(bg_audio.duration)

    # 이미지에 오디오 추가
    pose_img = pose_img.set_audio(bg_audio)

    # 비디오 저장 경로
    output_dir = "generated_videos"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"test_video_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
    output_path = os.path.join(output_dir, filename)

    # 비디오 파일 생성
    pose_img.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    # 임시 파일 삭제
    cleanup_tempfiles([pose_img_path, bg_audio_path])

    return output_path
