<!-- PROJECT LOGO -->
<br />
<p align="center">
  <!--<a href="https://github.com/hellmrf/WhatsGram-Stickers">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>
  -->
  <h1 align="center">WhatsGramStickers Bot</h1>

  <p align="center">
    Robô que converte figurinhas do WhatsApp para o Telegram de maneira fácil.
    <br />
    <a href="https://wa.me/553171352054?text=Hi"><strong>Testar »</strong></a>
    <br />
    <br />
    <a href="https://github.com/hellmrf/WhatsGram-Stickers/issues">Reporte uma falha</a>
    ·
    <a href="https://github.com/hellmrf/WhatsGram-Stickers">Read in English</a>
  </p>
</p>


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT LICENSE][LICENSE-shield]][LICENSE-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- TABLE OF CONTENTS -->
## Índice

* [Sobre o Projeto](#sobre-o-projeto)
  * [Feito com](#feito-com)
* [Começando](#começando)
  * [Pré-requisitos](#Pré-requisitos)
  * [Instalação](#Instalação)
* [Uso](#Uso)
  * [Primeira Execução](#primeira-execução)
* [Limitações](#Limitações)
* [Próximos passos](#Próximos-passos)
* [Como contribuir](#Como-contribuir)
* [Licença](#Licença)
* [Contato](#Contato)



<!-- Sobre o Projeto -->
## Sobre o Projeto

[![WhatsGramStickersBot Demonstration][product-screenshot]](https://wa.me/553171352054?text=Hello)

Muitas pessoas que migram para o Telegram, apesar da quantidade enorme de recursos comparado ao WhatsApp, sentem falta de algumas figurinhas que estão presentes no WhatsApp. Embora seja possível criar seu próprio pacote de figurinhas no Telegram, fazer isso com figurinhas já existentes no outro aplicativo não é. Pensando nisso, desenvolvi essa solução que, de maneira simples, permite que o usuário crie automaticamente um pacote no Telegram com suas figurinhas do WhatsApp. Como adicional, o pacote criado é legitimamente "propriedade" do usuário, podendo ser gerenciado normalmente, inclusive através do bot [@Stickers](http://t.me/Stickers).

Este projeto foi desenvolvido apenas para aprendizado. Como o último bot desenvolvido por mim utilizava Node.js, resolvi utilizar o Python dessa vez.
Durante o desenvolvimento, encontrei problemas como fazer com que o bot continuasse respondendo mensagens enquanto criava o pacote para um usuário, o que foi resolvido utilizando multithreading com o `concurrent.futures.ThreadPoolExecutor` do Python.
Fazer o _deploy_ do projeto também foi um desafio, já que o Heroku tem formas extremamente peculiares de funcionar.


### Feito com

Este projeto utiliza a linguagem [Python](https://www.python.org/), um banco de dados [PostgreSQL](https://www.postgresql.org/) e está hospedado gratuitamente no [Heroku](https://www.heroku.com/). 

Também utiliza os seguintes recursos:

* [Telegram Bot API](https://core.telegram.org/bots/api)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [WebWhatsAPI](https://github.com/mukulhase/WebWhatsapp-Wrapper/) (adaptado)

-------------
<!-- Começando -->
## Começando

Para obter uma cópia local e rodar seu próprio bot, siga esses passos simples.

### Pré-requisitos


* Certifique-se de possuir Python &geq; 3.7 e o pip.

* Você pode criar um [_virtual environment_](https://docs.python.org/3/tutorial/venv.html), mas é opcional.
```sh
$ python3 -m venv whatsgram

$ source tutorial-env/bin/activate # Unix

$ tutorial-env\Scripts\activate.bat # Windows
```

<small>**Dica para iniciantes**: você verá alguns commandos shell como esse: `(whatsgram) $ something`. Nesse caso, digita apenas `something` no seu Terminal. `(whatsgram)` indica o _virtual environment_ ativo e `$` indica "entrada".</small>

* Instale as dependências
```sh
(whatsgram) $ pip install -r requirements.txt
```

* [Instale PostgreSQL](https://www.postgresql.org/download/)

* Crie seu Bot com o [@BotFather](https://telegram.me/BotFather) e pegue seu token.

### Instalação
 
1. Clone o WhatsGram-Stickers entre no diretório
```sh
(whatsgram) $ git clone https://github.com/hellmrf/WhatsGram-Stickers.git

(whatsgram) $ cd WhatsGram-Stickers
```
2. Crie uma pasta `credentials` com dois arquivos: `database.ini` e `TelegramApiKey.txt` que contém o token do seu Bot no Telegram:
```sh
(whatsgram) $ mkdir credentials && cd credentials
(whatsgram) $ touch database.ini
(whatsgram) $ echo "TELEGRAM_TOKEN" > TelegramApiKey.txt
```
Se estiver usando Windows, use o Explorer e o Bloco de Notas (e tenha cuidado para salvar o database.ini como "Todos os arquivos", e não como "Plain text (*.txt)").

3. `database.ini` deve conter o seguinte (atualize pra fazer sentido no seu ambiente):

```ini
[postgresql]
host=localhost
database=whatsgram
user=postgres
password=postgres
```

4. Crie as tabelas necessárias

```sh
(whatsgram) $ python whatsgramstickers/migrate.py
```

--------------

<!-- Uso EXAMPLES -->
## Uso

Simplesmente execute

```sh
(whatsgram) $ python whatsgramstickers/main.py
```

### Primeira Execução

Na primeira execução, será necessário escanear o QR Code no WhatsApp Web. Você tem duas opções.

#### Primeira Opção: mais simples

Quando o bot tenta carregar o WhatsApp e falha, uma screenshot é obtida e salva em `whatsgramstickers/scrsht.png`. Simplesmente abra e escaneie.

#### Segunda Opção: mais confiável

Algumas vezes, o primeiro método obtém uma screenshot inútil (por exemplo, contendo apenas um spinner, ou um QR Code expirado). Nesse caso...

Abra `whatsgramstickers/main.py` e, por volta da linha 14, defina `headless=False` execute uma vez.
Chrome deve abrir o WhatsApp Web. Faça login como um usuário normal (garanta que "Mantenha-me conectado" está marcado).

Volte ao `main.py` e defina `headless=True` de volta (caso queira).

<!-- Próximos passos -->
## Limitações

As principais limitações são:

* Dispositivo móvel precisa estar sempre conectado à internet.
* O upload das figurinhas é feito em apenas uma _thread_ (no máximo duas, uma por usuário), o que torna esse processo extremamente demorado (veja a [issue #7](https://github.com/hellmrf/WhatsGram-Stickers/issues/7)).
* Embora o robô apague as mensagens com frequência, as figurinhas baixadas pelo dispositivo móvel continuam ocupando espaço.
* ~~O bot não responde o WhatsApp enquanto não conclui a geração de pacotes.~~ (resolvido)

## Próximos passos

Veja as [issues abertas](https://github.com/hellmrf/WhatsGram-Stickers/issues) pra uma lista de recursos propostos (e problemas conhecidos).


<!-- Como contribuir -->
## Como contribuir

Contribuições são o que tornam a comunidade open source um lugar tão incrível para aprender, se inspirar e criar. Qualquer contribuição é bem vinda.

1. Faça um fork do projeto
2. Crie uma nova branch (`git checkout -b feature/AmazingFeature`)
3. Commite suas alterações (`git commit -m 'Add some AmazingFeature'`)
4. Suba as alterações para o Github (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request



<!-- Licença -->
## Licença

Distribuido sob licença MIT. Veja [`LICENSE`][LICENSE-url] para mais informações.



<!-- Contato -->
## Contato

Heliton Martins - [@hellmrf](https://twitter.com/hellmrf) - helitonmrf@gmail.com

Link do projeto: [https://github.com/hellmrf/WhatsGram-Stickers](https://github.com/hellmrf/WhatsGram-Stickers)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/hellmrf/WhatsGram-Stickers.svg?style=flat-square
[contributors-url]: https://github.com/hellmrf/WhatsGram-Stickers/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/hellmrf/WhatsGram-Stickers.svg?style=flat-square
[forks-url]: https://github.com/hellmrf/WhatsGram-Stickers/network/members
[stars-shield]: https://img.shields.io/github/stars/hellmrf/WhatsGram-Stickers.svg?style=flat-square
[stars-url]: https://github.com/hellmrf/WhatsGram-Stickers/stargazers
[issues-shield]: https://img.shields.io/github/issues/hellmrf/WhatsGram-Stickers.svg?style=flat-square
[issues-url]: https://github.com/hellmrf/WhatsGram-Stickers/issues
[LICENSE-shield]: https://img.shields.io/github/license/hellmrf/WhatsGram-Stickers.svg?style=flat-square
[LICENSE-url]: https://github.com/hellmrf/WhatsGram-Stickers/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/helitonmrf
[product-screenshot]: screenshot.png