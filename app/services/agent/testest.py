from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
from google.cloud import texttospeech
from pydub import AudioSegment
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=OPENAI_API_KEY)

class TextToSpeechTool(BaseTool):
    name :str = "TextToSpeech Tool"
    description :str= "구글 텍스트to스피치 툴을 사용하여 요가 자세 설명을 음성으로 변환"

    def _run(self, text: str, posotion_mp3_name:str) -> str:
        try:
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text="네 발로 기어가듯 시작하여 손과 발을 바닥에 두고, 손은 어깨 너비로, 발은 엉덩이 너비로 벌린 뒤, 숨을 내쉬며 엉덩이를 하늘로 올리고, 다리와 팔을 곧게 펴며, 머리는 팔꿈치와 다리 사이에 두고, 발꿈치를 바닥으로 내리려 노력하며 이 자세를 유지하고 깊게 호흡합니다.")
            voice = texttospeech.VoiceSelectionParams(
                language_code="ko-KR",
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            with open(f"{posotion_mp3_name}.mp3", "wb") as out:
                out.write(response.audio_content)
            return "음성이 성공적으로 생성되어 저장되었습니다."
        except Exception as e:
            return f"[TextToSpeechTool] 에러: {str(e)}"

class MixMp3Tool(BaseTool):
    name:str = "MixMp3 Tool"
    description:str = "mp3를 합치는 툴"

    def _run(self, mp3_path_1: str) -> str:
        try:
            audio1 = AudioSegment.from_file(mp3_path_1)
            audio2 = AudioSegment.from_file('app/services/agents/forest_bird.mp3')
            combined = audio1.overlay(audio2, position=3000)
            combined.export("overlay_audio_delayed.mp3", format="mp3")
            return "mixed_mp3 completed"
        except Exception as e:
            return f"[MixMp3Tool] 에러: {str(e)}"

class AiLatestDevelopment:
    def __init__(self):
        self.agents_config = "config/agents.yaml"
        self.tasks_config = "config/tasks.yaml"

    def yoga_expert(self) -> Agent:
        return Agent(
            name="Yoga Expert",
            role="요가 전문가",
            goal="요가 자세를 추천하고 설명합니다",
            backstory="10년 경력의 요가 강사입니다",
            verbose=True,
            tools=[TextToSpeechTool(), MixMp3Tool()],
            llm=llm
        )

    def yoga_position_recommendation_task(self) -> Task:
        return Task(
            description="- TextToSpeechTool()를 이용해 요가 자세 안내 mp3를 생성. - TextToSpeechTool()로 생성된 {posotion_mp3_name}을 MixMp3Tool()의 매개변수로 전달합니다. -MixMp3Tool()를 사용하여 TextToSpeechTool()로 생성된 mp3와 배경 음악 mp3를 합쳐 하나의 mp3로 만듭니다. ",
            agent=self.yoga_expert(),
            expected_output="생성된 최종 mp3 파일의 경로"
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.yoga_expert()],
            tasks=[self.yoga_position_recommendation_task()],
            process=Process.sequential,
            verbose=True
        )

def run():
    ai_dev = AiLatestDevelopment()
    crew_instance = ai_dev.crew()
    result = crew_instance.kickoff()
    return result

if __name__ == "__main__":
    result = run()
    print(result)
