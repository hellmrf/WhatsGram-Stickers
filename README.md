<!-- PROJECT LOGO -->
<br />
<p align="center">
  <!--<a href="https://github.com/hellmrf/WhatsGram-Stickers">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>
  -->
  <h1 align="center">WhatsGramStickers Bot</h1>

  <p align="center">
    Bot that easily converts WhatsApp stickers to Telegram.
    <br />
    <a href="https://wa.me/553171352054?text=Hi"><strong>Try it »</strong></a>
    <br />
    <br />
    <a href="https://github.com/hellmrf/WhatsGram-Stickers/issues">Report Bug</a>
    ·
    <a href="https://github.com/hellmrf/WhatsGram-Stickers/blob/master/README.pt-BR.md">Leia em Português</a>
  </p>
</p>


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [First run](#first-run)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

[![WhatsGramStickersBot Demonstration][product-screenshot]](https://wa.me/553171352054?text=Hello)

Many people who migrate to Telegram, despite the huge amount of resources compared to WhatsApp, miss some stickers that are present on WhatsApp. While it's possible to create your own sticker pack on Telegram, doing so directly with WhatsApp stickers is not. With that in mind, I developed this solution that, in a simple way, allows the user to automatically create a package on Telegram with their WhatsApp stickers. As an additional feature, the created package is legitimately "owned" by the user and can be managed normally, including through the [@Stickers](http://t.me/Stickers) Bot.

This project was developed only for learning. As the last bot developed by me used Node.js, I decided to use Python this time.
During development, I encountered problems such as ensuring that the bot continues to respond to messages while creating the package for a user, which was solved using multithreading with Python's `concurrent.futures.ThreadPoolExecutor`.
Deploy the project was also a challenge, since Heroku has extremely peculiar ways of working.


### Built With

This project uses [Python](https://www.python.org/) as programming language, [PostgreSQL](https://www.postgresql.org/) as database and are free hosted on [Heroku](https://www.heroku.com/). 
It also uses the following resources.

* [Telegram Bot API](https://core.telegram.org/bots/api)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [WebWhatsAPI](https://github.com/mukulhase/WebWhatsapp-Wrapper/) (adapted)

-------------
<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites


* Make sure you have Python &geq; 3.7 and pip.

* You can create a new [virtual environment](https://docs.python.org/3/tutorial/venv.html), but it's optional
```sh
$ python3 -m venv whatsgram

$ source tutorial-env/bin/activate # Unix

$ tutorial-env\Scripts\activate.bat # Windows
```

<small>**Beginners tip**: you'll see shell commands like this: `(whatsgram) $ something`. In this case, type just `something` in your Terminal. `(whatsgram)` indicates the active virtual environment and `$` indicates "input".</small>

* Install dependencies
```sh
(whatsgram) $ pip install -r requirements.txt
```

* [Install PostgreSQL](https://www.postgresql.org/download/)

* Create your Telegram Bot with [@BotFather](https://telegram.me/BotFather) and get your token.

### Installation
 
1. Clone the WhatsGram-Stickers and enter the directoy
```sh
(whatsgram) $ git clone https://github.com/hellmrf/WhatsGram-Stickers.git

(whatsgram) $ cd WhatsGram-Stickers
```
2. Create a `credentials` folder with two files: `database.ini` and `TelegramApiKey.txt` that contain your Telegram Bot token:
```sh
(whatsgram) $ mkdir credentials && cd credentials
(whatsgram) $ touch database.ini
(whatsgram) $ echo "TELEGRAM_TOKEN" > TelegramApiKey.txt
```
If using Windows, use Explorer and Notepad (be sure to save database.ini as "All files", not "Text file (*.txt)").

3. `database.ini` will have the following content (update to match your environment):

```ini
[postgresql]
host=localhost
database=whatsgram
user=postgres
password=postgres
```

4. Create the necessary tables

```sh
(whatsgram) $ python whatsgramstickers/migrate.py
```

--------------

<!-- USAGE EXAMPLES -->
## Usage

Just run:

```sh
(whatsgram) $ python whatsgramstickers/main.py
```

### First run

For the first run, you'll need to scan the QR Code on WhatsApp Web. You have 2 choices.

#### First choice: the simplest

When the bot try to load to Whatsapp and fail, it'll take a screenshot of the browser and save to `whatsgramstickers/scrsht.png`. Just open and scan!

#### Second choice: the most reliable

Sometimes the first method takes an useless screenshot (just the spinner, for example). In this case...

Open `whatsgramstickers/main.py` and, on line 14, set `headless=False` and run once.
Chrome will open WhatsApp Web. 

Log in as a normal user (make sure "keep me connected" are checked).

Go back to `main.py` and set `headless=True` back.

## Limitations

The main limitations are:

* Mobile device must be always connected to the internet.
* Stickers are uploaded in only one thread (at most two, one per user), which makes this process extremely time-consuming (see [issue #7](https://github.com/hellmrf/WhatsGram-Stickers/issues/7)).
* Although the bot delete the messages when a new command are received, the stickers downloaded by mobile device continue eating space.
* ~~The bot doesn't respond to WhatsApp until it finishes generating a package~~ (fixed)


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/hellmrf/WhatsGram-Stickers/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Heliton Martins - [@hellmrf](https://twitter.com/hellmrf) - helitonmrf@gmail.com

Project Link: [https://github.com/hellmrf/WhatsGram-Stickers](https://github.com/hellmrf/WhatsGram-Stickers)


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
[license-shield]: https://img.shields.io/github/license/hellmrf/WhatsGram-Stickers.svg?style=flat-square
[license-url]: https://github.com/hellmrf/WhatsGram-Stickers/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/hellmrf
[product-screenshot]: screenshot.png