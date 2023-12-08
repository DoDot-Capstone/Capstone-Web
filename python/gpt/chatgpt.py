import openai
import re
import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import request, jsonify

# OpenAI API 키 설정
openai.api_key = "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"


def response(message):
    # GPT-3.5-turbo 모델을 사용하여 메시지에 대한 응답을 생성하는 함수
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "프로그래밍할 때 필요한 라이브러리를 추천해줍니다."},
            {"role": "user", "content": message},
            {"role": "user", "content": "프로그래밍할 때 필요한 라이브러리만 추천해줘야해, 무조건 라이브러리 이름에 해당하는 시작 부분에 '@'를 넣어주고 끝 부분에도 '@'를 넣어서 표시해줘 그리고 설명, 코드 자료는 필요 없어"}
        ],
        temperature=0,
        max_tokens=256
    )
    return response['choices'][0]['message']['content']


def extract_libraries(result):
    # GPT 응답에서 라이브러리 이름을 추출하는 함수
    extract_word = re.compile('@(.+?)@')
    return extract_word.findall(result)

def getGptReply():
    data = request.get_json()
    response_from_client = data.get('user_message')

    result = response(response_from_client)

    print(result)

    library_list = extract_libraries(result)

    return jsonify({'library_list': library_list})

if __name__ == "__main__":
    # 사용자로부터 메시지 입력
    message = input("물어봐: ")
    # GPT에 메시지 전달 및 라이브러리 추출
    result = response(message)

    library_list = extract_libraries(result)

    print("추천 라이브러리")
    for name in library_list:
        print(f" - {name}")

    yesno = input("상세하게 보시겠습니까?")

    if yesno.lower() == 'yes':
        search_libraries_in_mvn(library_list)
