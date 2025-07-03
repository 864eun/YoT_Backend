from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from datetime import datetime
import os

from app.utils.s3_tempfile import download_s3_to_tempfile, cleanup_tempfiles

async def create_pose_video(
    db,
    pose_ids: list,
    music_id: str,
    guide_labels: list
):
    # 파일 경로
    pose_img_url1 = "s3://yot-static-files/pose/Child's Pose.png"
    pose_img_url2 = "s3://yot-static-files/pose/Eagle.png"
    voice_url1 = "s3://yot-static-files/pose_voice/T아기자세보이스.mp3"
    voice_url2 = "s3://yot-static-files/pose_voice/T독수리자세.mp3"
    bg_music_url = "s3://yot-static-files/background_music/rain_1.mp3"

    # S3에서 임시 파일로 다운로드
    pose_img_path1 = download_s3_to_tempfile(pose_img_url1)
    pose_img_path2 = download_s3_to_tempfile(pose_img_url2)
    voice_path1 = download_s3_to_tempfile(voice_url1)
    voice_path2 = download_s3_to_tempfile(voice_url2)
    bg_audio_path = download_s3_to_tempfile(bg_music_url)

    temp_files = [pose_img_path1, pose_img_path2, voice_path1, voice_path2, bg_audio_path]

    try:
        # 오디오 로드
        voice1 = AudioFileClip(voice_path1)
        voice2 = AudioFileClip(voice_path2)
        bg_audio = AudioFileClip(bg_audio_path)

        # 각 이미지에 맞는 길이로 이미지 클립 생성
        base_clip = ImageClip(pose_img_path1)
        w, h = base_clip.size
        pose_img1 = base_clip.resized((w, h)).with_duration(voice1.duration)
        pose_img2 = ImageClip(pose_img_path2).resized((w, h)).with_duration(voice2.duration)

        # 오디오: 자세 보이스들은 순차적으로 붙이고, 배경음악은 전체 길이만큼 깔림
        total_duration = voice1.duration + voice2.duration

        # 자세 보이스를 순차적으로 이어붙임 (set_start 사용)
        voice2 = voice2.with_start(voice1.duration)
        voices = CompositeAudioClip([voice1, voice2])

        # 배경음악을 전체 길이만큼 자르고, 볼륨 낮추기(필요시)
        bg_audio = bg_audio.with_volume_scaled(0.2).subclipped(0, total_duration)

        # 두 오디오를 겹침
        final_audio = CompositeAudioClip([bg_audio, voices])

        # 이미지 비디오를 순차적으로 붙임
        video_clip = concatenate_videoclips([pose_img1, pose_img2])
        video_clip = video_clip.with_audio(final_audio)

        # 출력
        output_dir = "generated_videos"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"pose_voice_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
        output_path = os.path.join(output_dir, filename)

        video_clip.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )
    finally:
        cleanup_tempfiles(temp_files)
    return output_path
