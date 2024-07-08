$(document).ready(function(){
    var userId = {{ user_id|default:'null' }};

    if (userId) {
        function loadMessages() {
            $.ajax({
                url: '{% url "get_messages" user_id=0 %}'.replace('0', userId),
                method: 'GET',
                success: function(data) {
                    $('#chat-box').html('');
                    data.messages.forEach(function(msg) {
                        var messageDiv = $('<div>').addClass('message');
                        if (msg.sender === '{{ request.user.username }}') {
                            messageDiv.addClass('sent');
                        } else {
                            messageDiv.addClass('received');
                        }
                        messageDiv.html('<strong>' + msg.sender + '</strong>: ' + msg.message + ' <span>' + msg.timestamp + '</span>');
                        $('#chat-box').append(messageDiv);
                    });
                }
            });
        }

        $('#send-message-btn').click(function(){
            var message = $('#message-input').val();
            $.ajax({
                url: '{% url "chat_with_user" user_id=0 %}'.replace('0', userId),
                method: 'POST',
                data: {
                    'message': message,
                    'receiver_id': userId,
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                success: function(data) {
                    if (data.status === 'success') {
                        $('#message-input').val('');
                        loadMessages();
                    }
                }
            });
        });

        loadMessages();
        setInterval(loadMessages, 5000); // Reload messages every 5 seconds
    } else {
        $('#send-message-btn').prop('disabled', true);
        $('#message-input').prop('disabled', true);
    }
});