from moviepy import ImageClip, AudioFileClip
from datetime import datetime
import os

from app.utils.s3_tempfile import download_s3_to_tempfile, cleanup_tempfiles

async def create_pose_video(
    db,
    pose_ids: list,
    music_id: str,
    guide_labels: list
):
    pose_img_url = "s3://yot-static-files/pose/Eagle.png"
    bg_music_url = "s3://yot-static-files/background_music/rain_1.mp3"

    pose_img_path = download_s3_to_tempfile(pose_img_url)
    bg_audio_path = download_s3_to_tempfile(bg_music_url)

    # 오디오 파일 정상 여부 확인
    try:
        bg_audio = AudioFileClip(bg_audio_path).subclipped(0, 10)
        print("오디오 길이(초):", bg_audio.duration)
        print("오디오 채널 수:", bg_audio.nchannels)
        print("오디오 프레임레이트:", bg_audio.fps)
    except Exception as e:
        print("오디오 파일 로드 오류:", e)
        cleanup_tempfiles([pose_img_path, bg_audio_path])
        raise RuntimeError("오디오 파일에 문제가 있습니다.")

    # 이미지 클립 생성 (duration 파라미터로 지정)
    pose_img = ImageClip(pose_img_path, duration=bg_audio.duration)

    # audio 속성 할당 (moviepy 2.x 이상)
    pose_img.audio = bg_audio
    video_with_sound = pose_img

    output_dir = "generated_videos"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"test_video_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
    output_path = os.path.join(output_dir, filename)

    # 비디오 파일 생성
    video_with_sound.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        logger=None    # 필요시 logger 지정
    )

    cleanup_tempfiles([pose_img_path, bg_audio_path])

    return output_path
