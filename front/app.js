class Chatbox {
    // Definição do construtor da classe
    constructor() {
        // Argumentos para criação dos botoes no html na classe selecionada a partir do momento em que a classe é criada
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }
        // variaveis globais
        this.state = false;
        this.messages = [];
    }

    
    display() {
        const {openButton, chatBox, sendButton} = this.args;
        //Adicionando click 
        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        //se tiver aberta mostra a caixa se nao, nao
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    //Botao de envio
    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Bea", message: r.resposta, tag: r.tag, prob: r.prob};
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }

    //Atualizar o chat
    updateChatText(chatbox) {
        var html = '';
        //verifica se o item (mensagem) foi enviado pelo bot ou usuario pra mostrar no lado certo
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Bea")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '<br>'+ "Tag: " + item.tag + '<br>' +"Probabilidade: " + item.prob +  '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}


const chatbox = new Chatbox();
chatbox.display();