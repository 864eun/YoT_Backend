from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from datetime import datetime
import numpy as np
import os

from app.services.guide_voice.guide_voice_service import get_guide_voice_by_label
from app.services.pose.pose_service import get_pose_by_id
from app.services.pose_voice.pose_voice_serivce import get_pose_voice_by_pose_id
from app.services.music.music_service import get_music_by_id
from app.utils.s3_tempfile import download_s3_to_tempfile, cleanup_tempfiles, validate_s3_path


async def create_pose_video(
    db,
    pose_ids: list,
    music_id: str,
    guide_labels: list
):
    poses = await get_pose_by_id(db, pose_ids)
    music = await get_music_by_id(db, music_id)
    guide_voices = await get_guide_voice_by_label(db, guide_labels)
    
    pose_voices = []
    for pose_id in pose_ids:
        voices = await get_pose_voice_by_pose_id(db, pose_id)
        pose_voices.append(voices[0] if voices else None)

    # --- 데이터 상태 로그 출력 추가 ---
    print(f"Poses count: {len(poses)}")
    for pose in poses:
        print(f"Pose ID: {pose.pose_id}, URL: {pose.url}")

    if music:
        print(f"Music ID: {music.music_id}, URL: {music.url}")
    else:
        print("Music not found")

    print(f"Guide voices count: {len(guide_voices)}")
    for gv in guide_voices:
        print(f"GuideVoice ID: {gv.guide_voice_id}, Label: {gv.label}, URL: {gv.url}")

    for i, pv in enumerate(pose_voices):
        if pv:
            print(f"PoseVoice {i} URL: {pv.url}")
        else:
            print(f"PoseVoice {i} is None")
    # -----------------------------------

    # S3 경로 검증
    invalid_paths = []

    for pose in poses:
        if not validate_s3_path(pose.url):
            invalid_paths.append(f"Pose ID {pose.pose_id} - Invalid S3 path: {pose.url}")

    if music and not validate_s3_path(music.url):
        invalid_paths.append(f"Music ID {music.music_id} - Invalid S3 path: {music.url}")

    for gv in guide_voices:
        if not validate_s3_path(gv.url):
            invalid_paths.append(f"GuideVoice ID {gv.guide_voice_id} - Invalid S3 path: {gv.url}")

    for pv in pose_voices:
        if pv and not validate_s3_path(pv.url):
            invalid_paths.append(f"PoseVoice Invalid S3 path: {pv.url}")

    if invalid_paths:
        error_msg = "Invalid S3 paths detected:\n" + "\n".join(invalid_paths)
        raise ValueError(error_msg)

    clips = []
    audios = []
    temp_files = []

    # 시작 가이드
    if start_guide := next((gv for gv in guide_voices if gv.label == "start"), None):
        start_audio_path = download_s3_to_tempfile(start_guide.url)
        temp_files.append(start_audio_path)
        start_audio = AudioFileClip(start_audio_path)
        start_clip = ImageClip(
            np.zeros((1080, 1920, 3), dtype=np.uint8),
            duration=start_audio.duration
        )
        start_clip.audio = start_audio
        clips.append(start_clip)
        audios.append(start_audio)

    # 포즈 시퀀스
    for i, pose in enumerate(poses):
        pose_img_path = download_s3_to_tempfile(pose.url)
        temp_files.append(pose_img_path)
        
        if pose_voices[i]:
            pose_audio_path = download_s3_to_tempfile(pose_voices[i].url)
            temp_files.append(pose_audio_path)
            pose_audio = AudioFileClip(pose_audio_path)
            pose_img = ImageClip(pose_img_path, duration=pose_audio.duration)
            pose_img.audio = pose_audio
            audios.append(pose_audio)
        else:
            pose_img = ImageClip(pose_img_path, duration=5)
            
        clips.append(pose_img)
        
        if i < len(poses) - 1 and (sec_guide := next((gv for gv in guide_voices if gv.label == "count10s"), None)):
            sec_audio_path = download_s3_to_tempfile(sec_guide.url)
            temp_files.append(sec_audio_path)
            sec_audio = AudioFileClip(sec_audio_path)
            sec_clip = ImageClip(
                np.zeros((1080, 1920, 3), dtype=np.uint8),
                duration=sec_audio.duration
            )
            sec_clip.audio = sec_audio
            clips.append(sec_clip)
            audios.append(sec_audio)

    # 배경 음악
    if music:
        bg_audio_path = download_s3_to_tempfile(music.url)
        temp_files.append(bg_audio_path)
        bg_audio = AudioFileClip(bg_audio_path)
        total_duration = sum(clip.duration for clip in clips)
        if bg_audio.duration < total_duration:
            bg_audio = bg_audio.audio_loop(duration=total_duration)
        else:
            bg_audio = bg_audio.subclipped(0, total_duration)
        final_audio = CompositeAudioClip([*audios, bg_audio])
    else:
        final_audio = CompositeAudioClip(audios)

    # 최종 영상 생성
    final_video = concatenate_videoclips(clips)
    final_video.audio = final_audio

    output_dir = "generated_videos"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"pose_video_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
    output_path = os.path.join(output_dir, filename)
    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    cleanup_tempfiles(temp_files)
    return output_path
