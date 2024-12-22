const current_user_id = JSON.parse(document.getElementById('user_id').textContent)

<!--функция для получения списка и содержимого чатов юзера-->
async function getChats(url) {
    const response = await fetch(url);
    return await response.json();
}


<!--функция для автоскролинга в конец диалога-->
async function scrollToBottom(elementId) {
    var div = document.getElementById(elementId);
    div.scrollTop = div.scrollHeight;
}


<!--функция генерации блоков сообщений-->
async function displayNewMessage(content, author, authorID, time, avatar, divDialogContainer) {
    let divMessageContainer = document.createElement('div');
    let divMessage = document.createElement('div');
    let divContent = document.createElement('div');
    let divAuthor = document.createElement('div');
    let divAvatar = document.createElement('div');
    let avatarImage = document.createElement('img');
    let divTime = document.createElement('div');


    if (currentUserID == authorID) {
        divMessageContainer.className = 'message_container_right';
        divMessage.className = 'message_right'
    } else if (currentUserID != authorID) {
        divMessageContainer.className = 'message_container_left';
        divMessage.className = 'message_left'
    }
    divContent.className = 'message_content';
    divAuthor.className = 'message_author';
    divTime.className = 'message_time';
    avatarImage.className = 'user_avatar_chat';

    divContent.innerHTML = `${content}`;
    divAuthor.innerHTML = `${author}`;
    divTime.innerHTML = `${time}`;
    avatarImage.src = avatar;


    divDialogContainer.appendChild(divMessageContainer)
    divMessageContainer.appendChild(divMessage)
    divMessage.appendChild(divAuthor);
    divAvatar.appendChild(avatarImage);
    divMessage.appendChild(divAvatar);
    divMessage.appendChild(divContent);
    divMessage.appendChild(divTime);
}


<!--функция генерации формы отправки сообщений-->
async function createSendMessageForm(chatID, chatWindow, chatSocket) {
    let divInputField = document.createElement('div');
    divInputField.className = 'input_field';

    let sendMessageForm = document.createElement('form');
    sendMessageForm.id = "send_message_form";
    sendMessageForm.className = "send_message_form";

    let textField = document.createElement ('textarea');
    textField.className = "text_field";
    textField.placeholder = "Введите сообщение";
    textField.name = "content";

    let chatNumber = document.createElement('input');
    chatNumber.type = "hidden";
    chatNumber.name = "chat";
    chatNumber.value = chatID;

    let sendMessageButton = document.createElement('button');
    sendMessageButton.className = "send_message_button";
    sendMessageButton.type = "submit";
    sendMessageButton.innerText = "Отправить";

    let userID = document.createElement('input');
    userID.type = "hidden";
    userID.name = "author";
    userID.value = current_user_id;

    chatWindow.appendChild(divInputField)
    divInputField.appendChild(sendMessageForm);
    sendMessageForm.appendChild(textField);
    sendMessageForm.appendChild(sendMessageButton);
    sendMessageForm.appendChild(chatNumber);
    sendMessageForm.appendChild(userID);

            <!--прослушка события отправки сообщения из формы-->
    sendMessageForm.addEventListener('submit', async event => {
        event.preventDefault();
        let formData = new FormData(sendMessageForm);
        let plainFormData = Object.fromEntries(formData.entries());
        plainFormData['time'] = new Date();
        let formDataJsonString = JSON.stringify(plainFormData);
        try {
            const response = await fetch('http://127.0.0.1:8000/api/chatMessages/', {
                method: 'POST',
                body: formDataJsonString,
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
            });
            const fetchData = await response.json();
            } catch (error) {
                console.error(error);
        }
        textField.value = ""
        chatSocket.send(formDataJsonString);
    })
}


<!--Получение отображаемого названия чата-->
async function generateChatName(chat) {
    let chatType = chat.type;
    let userList = chat.users;
    let users = [];
    console.log(chat.users)
    if (chatType == "DIALOG"){
        for (let user = 0; user < chat.users.length; user++){
            console.log(chat.users[user].id, currentUserID)
            console.log(chat.users[user].id == currentUserID)
            if (chat.users[user].id != currentUserID){
                let chatName = chat.users[user].username;
                return chatName
            }
        }
    } else {
        for (let user = 0; user < chat.users.length; user++){
            users.push(chat.users[user].username);
        }
        let chatName = users.join(', ');
        return chatName
    }
}


<!--Получение списка сообщений, отрисовка содержимого чата-->
async function getMessageFromChat(chatID, chatName, chatType) {
    let url = `http://127.0.0.1:8000/api/chatMessages?id=${chatID}`;
    const response = await fetch(url);
    let messages = await (response.json());

    const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/livechat/' + chatID + '/');

    let chatWindow = document.getElementById('chat_window');
    chatWindow.innerHTML = '';

    let divChatHeader = document.createElement('div');
    divChatHeader.className  = 'chat_header';
    divChatHeader.id = 'chat_header';

    let divChatNameContainer  = document.createElement('div');
    divChatNameContainer.className  = 'chat_name_container';
    divChatNameContainer.id = 'chat_name_container';
    divChatNameContainer.innerHTML = `${chatName}`;

    let divDialogContainer = document.createElement('div');
    divDialogContainer.className = 'dialog_container';
    divDialogContainer.id = 'div_dialog_container';

    divChatHeader.appendChild(divChatNameContainer)
    if (chatType == "GROUP_CHAT") {
        let addUserFormBox = document.createElement('div');
        addUserFormBox.className = 'add_user_form_box';

        let addUserForm = document.createElement('form');
        addUserForm.id = "add_user_form";
        addUserForm.className = "add_user_form";

        let chatNumber = document.createElement('input');
        chatNumber.type = "hidden";
        chatNumber.name = "chatID";
        chatNumber.value = chatID;

        let searchField = document.createElement('input');
        searchField.className = 'adding_user_input_field'
        searchField.id = "searchField"
        searchField.name = "username";
        searchField.placeholder = "Пригласить пользователя";

        let searchResult = document.createElement('div');
        searchResult.className = "search_result"
        searchResult.id = "searchResult"
        searchResult.name = "searchResult";


        addUserForm.appendChild(searchField)
        addUserForm.appendChild(chatNumber)
        addUserFormBox.appendChild(addUserForm)
        addUserFormBox.appendChild(searchResult)
        divChatHeader.appendChild(addUserFormBox)

        addUserForm.addEventListener("keyup", event => {
            console.log(event.target.value)
            searchResult.innerHTML = ''
            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:8000/addUserSearch/",
                data: {
                    "text": event.target.value,
                    'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                success: (res) => {
                    console.log(res);
                    searchResult.innerHTML = ''
                    if (res.data != "Пользователи не найдены" && searchField.value.length > 0){
//                        currentUserID = current_user_id;
                        for (let user = 0; user < res.data.length; user++){
                            let userVariantBox = document.createElement('form');
                            userVariantBox.className = "search_result_variant_box";

                            let userVariantName = document.createElement('div');
                            userVariantName.className = 'search_result_variant_username';
                            userVariantName.innerHTML = res.data[user].username;


                            let userVariantAddingButton = document.createElement('button');
                            userVariantAddingButton.type = 'submit';
                            userVariantAddingButton.className  = 'search_result_variant_adding_button';
                            userVariantAddingButton.innerHTML = 'Добавить';


                            userVariantBox.appendChild(userVariantName);
                            if (res.data[user].id != currentUserID){
                                userVariantBox.appendChild(userVariantAddingButton);
                            }
                            searchResult.appendChild(userVariantBox);

                            userVariantBox.addEventListener("submit", event => {
                                searchResult.innerHTML = ''
                                $.ajax({
                                    type: "POST",
                                    url: "http://127.0.0.1:8000/addingUser/",
                                    data: {
                                        'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                                        "userID": res.data[user].id,
                                        "chatNumber": chatID,
                                    },
                                    success: (res) => {
                                        if (res.data == "Пользователь уже добавлен в чат ранее"){
                                            searchResult.innerHTML = res.data;
                                        }
                                        else {
                                            searchResult.innerHTML = res.data.result;
                                            generateChatName(chat, chats)
                                        }
                                    },
                                    error: (err) =>{
                                        console.log(err);
                                    }
                                })
                            })
                        }
                    }
                    else if (res.data == "Пользователи не найдены" && searchField.value.length > 0){
                        searchResult.innerHTML = res.data;
                    }
                    else {
                        searchResult.innerHTML= ''
                    }
                },
                error: (err) =>{
                    console.log(err);
                }
            })
        })

    }
    chatWindow.appendChild(divChatHeader)
    chatWindow.appendChild(divDialogContainer)



    for (let message = 0; message < messages.length; message++){
        let content = messages[message].content;
        let author = messages[message].author.username;
        let authorID = messages[message].author.id;
        let time = messages[message].time;
        let avatar = messages[message].author.avatar;
        console.log(`это аватарка ${avatar}`)
        var chat  = messages[message].chat;

        await displayNewMessage(content, author, authorID, time, avatar, divDialogContainer);
    }

    await createSendMessageForm (chatID, chatWindow, chatSocket);

                <!--прослушка события получения сообщения по WS-->
    chatSocket.onmessage = async function(e) {
        const socketData = JSON.parse(e.data);
        console.log(socketData)
        let content = socketData.content
        let author = socketData.author
        let authorID = socketData.authorID
        let time = socketData.time
        let avatar = socketData.avatar
        console.log(time)
        await displayNewMessage(content, author, authorID, time, avatar, divDialogContainer)
        await scrollToBottom('div_dialog_container')
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    await scrollToBottom('div_dialog_container')
}


<!--получение всех чатов юзера при открытии страницы-->
(async () => {
//    let currentUserID = current_user_id;
    let chats = await getChats('http://127.0.0.1:8000/api/userChats/')

    let currentUrl = window.location.href.split('/', 5)
    let chatForOpen = currentUrl[4]

    for (let chat = 0; chat < chats.length; chat++){
        let chatID = chats[chat].id;
        let chatType = chats[chat].type;
        let chatName = await generateChatName(chats[chat])

        let divChat = document.createElement('div');
        divChat.className = 'chat';
        divChat.innerHTML = `${chatName}`;
        divChat.onclick = await function(){
            let chatName = divChat.innerText;
            getMessageFromChat(chatID, chatName, chatType);
            console.log(chatID)
        }
        chatContainer = document.getElementsByClassName('chat_container')[0];
        chatContainer.appendChild(divChat)
        if (chatForOpen != '' && chatForOpen == chatID) {
            getMessageFromChat(chatForOpen, chatName, chatType);
        }
    }
})();
