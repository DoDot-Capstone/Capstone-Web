// Add an event listener to the input element
var inputElement = document.getElementById('input-message');
inputElement.addEventListener('keydown', function(event) {
    // Check if the pressed key is Enter (keyCode 13)
    if (event.keyCode === 13) {
        // Call the sendMessage function
        sendMessage();
    }
});

// Your existing sendMessage function
function sendMessage() {
    var inputElement = document.getElementById('input-message');
    var message = inputElement.value.trim();

    if (message !== '') {
        var outputElement = document.getElementById('chat-output');

        // 사용자 입력 메시지 표시
        outputElement.innerHTML += '<div class="user-message">' + message + '</div>';

        // 가상의 응답 (실제로는 서버로 메시지를 보내고 응답을 받는 로직으로 대체해야 함)
        var response = "SSD: 안녕하세요! 어떻게 도와드릴까요?";

        // 챗 GPT 응답 메시지 표시
        outputElement.innerHTML += '<div class="gpt-message">' + response + '</div>';

        // 입력창 초기화
        inputElement.value = '';

        // 스크롤을 가장 아래로 이동
        outputElement.scrollTop = outputElement.scrollHeight;
    }
}