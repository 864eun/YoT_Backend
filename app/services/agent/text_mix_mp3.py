from pydub import AudioSegment

# 오디오 파일 로드
audio1 = AudioSegment.from_file('forest_bird.mp3')
audio2 = AudioSegment.from_file('output.mp3')

# 두 번째 오디오를 3초 지점부터 겹치기
combined = audio1.overlay(audio2, position=3000)  # 3000ms = 3초

# 결과 저장
combined.export("overlay_audio_delayed.mp3", format="mp3")
