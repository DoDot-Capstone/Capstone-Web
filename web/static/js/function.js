// 입력 요소에 이벤트 리스너 추가
var inputElement = document.getElementById('input-message');
inputElement.addEventListener('keydown', function(event) {
    // 눌린 키가 Enter인지 확인 (keyCode 13)
    if (event.keyCode === 13) {
        // Enter 키가 눌렸을 때 sendMessage 함수 호출
        sendMessage();
    }
});


function sendMessage() {
    // ID를 통해 입력 요소 가져오기
    var inputElement = document.getElementById('input-message');
    // 입력 값의 앞뒤 공백을 제거한 값을 가져오기
    var message = inputElement.value.trim();

    if (message !== '') {
        // ID를 통해 채팅 출력 요소 가져오기
        var outputElement = document.getElementById('chat-output');

        // 사용자의 입력 메시지를 채팅에 표시
        outputElement.innerHTML += '<div class="user-message">' + message + '</div>';

        // 가상의 응답 (실제로는 서버로 메시지를 보내고 응답을 받는 로직으로 대체해야 함)
        var response = "SSD: 안녕하세요! 어떻게 도와드릴까요?";

        // 챗 응답 메시지 표시
        outputElement.innerHTML += '<div class="gpt-message">' + response + '</div>';

         // 메시지를 보낸 후 입력창 초기화
        inputElement.value = '';

         // 채팅 출력을 가장 아래로 스크롤하여 최신 메시지를 표시
        outputElement.scrollTop = outputElement.scrollHeight;
    }
}