const formulario = document.getElementById('form-login'); //1 seleciona o formulario

formulario.addEventListener('submit', async (event) => { //1 adiciona um ouvinte de evento para o envio do formulario
    event.preventDefault();//1 previne o comportamento padrão do formulario
    
    const login = document.getElementById('login').value;//1 pega o valor do campo de login
    const senha = document.getElementById('senha').value;//1 pega o valor do campo de senha

    // Enviar dados para o servidor
    const response = await fetch('/login', { //1 envia os dados para o servidor usando fetch
        method: 'POST', //1 método POST para enviar os dados
        headers: { //1 define o cabeçalho para indicar que os dados estão em formato JSON
            'Content-Type': 'application/json' //1 indica que o corpo da requisição é JSON
        },
        body: JSON.stringify({ login, senha }) //1 converte os dados em JSON e os envia no corpo da requisição
    });

    const data = await response.json(); //1 espera a resposta do servidor e a converte para JSON

    if (data.success) { //1 verifica se o login foi bem-sucedido
        window.location.href = '/menu'; //1 redireciona para a página do dashboard se o login for bem-sucedido
    } else {
        alert(data.message); //1 exibe uma mensagem de erro se o login falhar
    }
});

function depositar() {
    const valor = document.getElementById('valor-deposito').value;
    // Lógica para enviar o valor de depósito para o servidor
    // Exemplo: await fetch('/depositar', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ valor }) });
    const response = await fetch('/depositar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Indica que o corpo da requisição é JSON
        },
        body: JSON.stringify({ valor })
    });

    const data = await response.json();

    if (data.success) {
        alert('Depósito realizado com sucesso!');
        // Atualizar o saldo na interface, se necessário
    } else {
        alert('Erro ao realizar depósito: ' + data.message);
    }
}