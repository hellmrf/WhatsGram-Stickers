# Conventions

Here we'll define all the conventions for the system.

## Stages

Users always have a stage that indicates what the bot has to do with incoming messages. 

* [0] Unknown

  Either user doesn't exists or have completed all requests. Bot answer with welcome message and menu.  

* [1] Package_title

  Read package Title

* [2] Package_name

  Read package name

* [3] Get stickers

  User is sending stickers. Bot will only wait for `/done`.
  
* [4] Get emojis

  Bot will read emojis and start the process. If ok, send confirmation and tell user how to get stickers on Telegram. Sets `stage` back to `0`.

## Bot Messages

Here are all planned conversation.

------------------

### `wellcome` (`stage == 0`)

> Olá! Eu sou um robô 🤖 e consigo enviar figurinhas aqui do Whatsapp para o Telegram.
  Para começar, envie `/start`

------------------

### `start` (`stage == 1`)


> Ótimo, me envie agora o nome do pacote que você deseja criar no Telegram.

------------------

### `package_name` (`stage == 2`)

> Me envie também um id para seu pacote. Ele pode conter apenas letras (sem acentos), "_" e números, e precisa começar com uma letra. 
>
> Seu pacote de stickers será adicionado usando um link como: t.me/addstickers/seu_id_aqui. 

------------------

### `send_me_stickers` (`stage == 3`)

> Ok. Agora me envie todas as figurinhas que você quer adicionar ao pacote *<pack>*. 
  Quando terminar, envie `/done`

------------------

### `send_me_emojis` (`stage == 4`)
Após `/done`

> Estamos quase lá. No Telegram, cada figurinha tem um emoji associado. Por favor, me envie os emojis correspondentes às suas figurinhas, na mesma ordem que me enviou.
  Aqui você tem algumas opções:
  - Enviar apenas um emoji (e todos os stickers vão referenciar o mesmo emoji);
  - Enviar, na mesma mensagem, um emoji para cada figurinha;
  - Enviar, na mesma mensagem, quantos emojis quiser, mas uma linha para cada figurinha.
  
------------------

### `whats_your_telegram` 

> Tudo certo! Concluimos a criação do seu pack de figurinhas. Para adicionar ao telegram, use o link a seguir: .... 

------------------

### `done`

> Pronto! Te enviei no Telegram uma figurinha do seu pack. Clique/toque sobre ela e escolha "Adicionar stickers" para salvar.
