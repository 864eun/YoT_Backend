from google.cloud import texttospeech

# 클라이언트 객체 생성
client = texttospeech.TextToSpeechClient()

# 변환할 텍스트 설정
synthesis_input = texttospeech.SynthesisInput(text="안녕하세요, 반갑습니다.")

# 음성 설정 (한국어, 여성 음성)
voice = texttospeech.VoiceSelectionParams(
    language_code="ko-KR", 
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)

# 오디오 설정 (MP3 형식)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# 텍스트를 음성으로 변환
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# 결과를 파일로 저장
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')
