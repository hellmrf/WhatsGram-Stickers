# Bot Messages

Here are all planned conversation.

------------------

### `wellcome`

> Olá! Eu sou um robô 🤖 e consigo enviar figurinhas aqui do Whatsapp para o Telegram.
  Para começar, envie `/start`

------------------

### `start`


> Ótimo, me envie agora o nome do pacote que você deseja criar no Telegram.

------------------

### `send_me_stickers`

Após `/start`, escutar pelo nome do pacote


> Ok. Agora me envie todas as figurinhas que você quer adicionar ao pacote *<pack>*. 
  Quando terminar, envie `/done`

------------------

### `send_me_emojis`
Após `/done`

> Estamos quase lá. No Telegram, cada figurinha tem um emoji associado. Por favor, me envie os emojis correspondentes às suas figurinhas, na mesma ordem que me enviou.
  Aqui você tem algumas opções:
  - Enviar apenas um emoji (e todos os stickers vão referenciar o mesmo emoji);
  - Enviar, na mesma mensagem, um emoji para cada figurinha;
  - Enviar, na mesma mensagem, quantos emojis quiser, mas uma linha para cada figurinha.
  
------------------

### `whats_your_telegram`

> Certo. Agora, preciso que me informe o seu número ou usuário do Telegram. Tenha atenção, pois se informar um número inválido, teremos que fazer tudo de novo.

------------------

### `done`

> Pronto! Te enviei no Telegram uma figurinha do seu pack. Clique/toque sobre ela e escolha "Adicionar stickers" para salvar.
