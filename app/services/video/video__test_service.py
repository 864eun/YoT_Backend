from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from datetime import datetime
import numpy as np
import os
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.guide_voice.guide_voice_service import get_guide_voice_by_label
from app.services.pose.pose_service import get_pose_by_id
from app.services.pose_voice.pose_voice_serivce import get_pose_voice_by_pose_id
from app.services.music.music_service import get_music_by_id

async def create_pose_video(
    db: AsyncSession,
    pose_ids: list,        # 포즈 ID 리스트 (단수/복수)
    music_id: str,         # 음악 ID (단수)
    guide_labels: list     # 가이드 보이스 라벨 (['start', 'count10s'])
):
    # 1. 데이터베이스에서 필요한 데이터 가져오기
    poses = await get_pose_by_id(db, pose_ids)
    music = await get_music_by_id(db, music_id)
    guide_voices = await get_guide_voice_by_label(db, guide_labels)
    
    # 2. 포즈 음성 가져오기
    pose_voices = []
    for pose_id in pose_ids:
        voices = await get_pose_voice_by_pose_id(db, pose_id)
        pose_voices.append(voices[0] if voices else None)  # 첫 번째 음성 사용

    # 3. 가이드 보이스 분류
    start_guide = next((gv for gv in guide_voices if gv.label == "start"), None)
    sec_guide = next((gv for gv in guide_voices if gv.label == "count10s"), None)

    # 4. 동영상 클립 생성
    clips = []
    audios = []

    # 시작 가이드 섹션
    if start_guide:
        start_audio = AudioFileClip(start_guide.url)
        start_clip = ImageClip(np.zeros((1080, 1920, 3), dtype=np.uint8), duration=start_audio.duration)
        start_clip.audio = start_audio  # 수정
        clips.append(start_clip)
        audios.append(start_audio)

    # 포즈 시퀀스 섹션
    for i, pose in enumerate(poses):
        # 포즈 이미지 클립
        pose_img = ImageClip(pose.url)
        
        # 포즈 음성 처리
        pose_audio = None
        if pose_voices[i]:
            pose_audio = AudioFileClip(pose_voices[i].url)
            pose_img = pose_img.set_duration(pose_audio.duration)
            pose_img.audio = pose_audio  # 수정
            audios.append(pose_audio)
        else:
            pose_img = pose_img.set_duration(5)  # 기본 5초 지속
        
        clips.append(pose_img)
        
        # 포즈 사이 초 가이드 (마지막 포즈 제외)
        if i < len(poses) - 1 and sec_guide:
            sec_audio = AudioFileClip(sec_guide.url)
            sec_clip = ImageClip(np.zeros((1080, 1920, 3), dtype=np.uint8), duration=sec_audio.duration)
            sec_clip.audio = sec_audio  # 수정
            clips.append(sec_clip)
            audios.append(sec_audio)

    # 5. 배경 음악 처리
    if music:
        bg_audio = AudioFileClip(music.url)
        total_duration = sum(clip.duration for clip in clips)
        
        # 배경음 길이 조정
        if bg_audio.duration < total_duration:
            bg_audio = bg_audio.audio_loop(duration=total_duration)
        else:
            bg_audio = bg_audio.subclip(0, total_duration)
        
        # 오디오 믹싱
        final_audio = CompositeAudioClip([*audios, bg_audio])
    else:
        final_audio = CompositeAudioClip(audios)

    # 6. 최종 동영상 생성
    final_video = concatenate_videoclips(clips)
    final_video.audio = final_audio  # 수정
    
    # 7. 파일 출력
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
    
    return output_path