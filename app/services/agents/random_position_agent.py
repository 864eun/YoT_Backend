import requests
from crewai import Agent, Crew, Process, Task
from crewai.project import agent,task, CrewBase, crew
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI 
from crewai.tools import BaseTool
from google.cloud import texttospeech
from pydantic import BaseModel, Field
from typing import Optional
from pydub import AudioSegment




load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=OPENAI_API_KEY)

#자세 검색 및 설명 툴



#텍스트 -> 스피치 툴
class TextToSpeechTool(BaseModel):
    name: str = "TextToSpeechTool"
    
    description: str = "구글 텍스트to스피치 툴을 사용하여 요가 자세 설명을 음성으로 변환"

    
    def _run(self) -> str:
        try:
            client = texttospeech.TextToSpeechClient()

            # 텍스트 입력
            synthesis_input = texttospeech.SynthesisInput(text="네 발로 기어가듯 시작하여 손과 발을 바닥에 두고, 손은 어깨 너비로, 발은 엉덩이 너비로 벌린 뒤, 숨을 내쉬며 엉덩이를 하늘로 올리고, 다리와 팔을 곧게 펴며, 머리는 팔꿈치와 다리 사이에 두고, 발꿈치를 바닥으로 내리려 노력하며 이 자세를 유지하고 깊게 호흡합니다.")
            
            # 음성 설정
            voice = texttospeech.VoiceSelectionParams(
                language_code="ko-KR",
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            
            # 오디오 설정
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            # 텍스트를 음성으로 변환
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            
            # 오디오 파일로 저장
            with open("output_2.mp3", "wb") as out:
                out.write(response.audio_content)
            
            return f"음성이 성공적으로 생성되어 저장되었습니다."
        
        except Exception as e:
            return f"[TextToSpeechTool] 에러: {str(e)}"

        
# 배경 음악 가져오는 툴


# 배경 mp3과 음성 mp3 합치는 툴
class MixMp3Tool(BaseTool) :
    name:str = "MixMp3Tool",
    description:str="mp3를 합치는 툴"

    def _run(self, mp3_path_1 :str) -> str :
        try:
            audio1 = AudioSegment.from_file('mp3_path_1')
            audio2 = AudioSegment.from_file('app/services/agents/forest_bird.mp3')

            # 두 번째 오디오를 3초 지점부터 겹치기
            combined = audio1.overlay(audio2, position=3000)  # 3000ms = 3초

            # 결과 저장
            combined.export("overlay_audio_delayed.mp3", format="mp3")
                
            return "mixed_mp3 completed"
        except Exception as e:
            return f"[MixMp3ToolTool] 에러: {str(e)}"


# crew 정의 
@CrewBase
class AiLatestDevelopment():

    agents_config = "config/agents.yaml" 
    tasks_config = "config/tasks.yaml"

    @agent
    def yoga_expert(self) -> Agent:
        return Agent(
            config= self.agents_config['yoga_expert'],
            verbose=True,
            tools=[TextToSpeechTool(), MixMp3Tool()],
            manager_llm=llm 
        )

    @task
    def yoga_posotion_recommendation_task(self) -> Task:
        return Task(
            config=self.tasks_config['yoga_posotion_recommendation_task']
        )
        
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.yoga_expert()],
            tasks=[self.yoga_posotion_recommendation_task()],
            process=Process.sequential,
            verbose=True
        )

def run():

    ai_dev = AiLatestDevelopment()
    crew_instance = ai_dev.crew()
    
    result = crew_instance.kickoff()
    return result