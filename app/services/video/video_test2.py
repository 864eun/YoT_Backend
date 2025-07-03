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
    pose_img_url1 = "s3://yot-static-files/pose/Child's Pose.png"
    pose_img_url2 = "s3://yot-static-files/pose/Eagle.png"
    start_voice_url = "s3://yot-static-files/guide_voice/T시작호흡.mp3"
    bg_music_url = "s3://yot-static-files/background_music/rain_1.mp3"

    pose_img_path1 = download_s3_to_tempfile(pose_img_url1)
    pose_img_path2 = download_s3_to_tempfile(pose_img_url2)
    start_voice_path = download_s3_to_tempfile(start_voice_url)
    bg_audio_path = download_s3_to_tempfile(bg_music_url)

    temp_files = [pose_img_path1, pose_img_path2, start_voice_path, bg_audio_path]

    try:
        start_voice = AudioFileClip(start_voice_path)
        bg_audio = AudioFileClip(bg_audio_path)
        print("시작오디오 길이:", start_voice.duration, "채널:", start_voice.nchannels, "fps:", start_voice.fps)
        print("배경음악 길이:", bg_audio.duration, "채널:", bg_audio.nchannels, "fps:", bg_audio.fps)
    except Exception as e:
        cleanup_tempfiles(temp_files)
        print("오디오 파일 로드 오류:", e)
        raise RuntimeError("오디오 파일에 문제가 있습니다.")

    # 볼륨 조정 (MoviePy 2.x)
    start_voice = start_voice.with_volume_scaled(2.0)

    # CompositeAudioClip 생성 및 길이 자르기
    composite_audio = CompositeAudioClip([
        bg_audio,
        start_voice.with_start(0)
    ]).subclipped(0, 20)

    # 이미지 클립 생성 (각 10초)
    base_clip = ImageClip(pose_img_path1, duration=10)
    w, h = base_clip.size
    pose_img1 = base_clip
    pose_img2 = ImageClip(pose_img_path2, duration=10).resized((w, h))

    video_clip = concatenate_videoclips([pose_img1, pose_img2])
    video_clip.audio = composite_audio

    output_dir = "generated_videos"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"test_voice_and_music_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
    output_path = os.path.join(output_dir, filename)

    video_clip.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    cleanup_tempfiles(temp_files)
    return output_path
