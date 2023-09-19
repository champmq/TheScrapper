# TheScrapper

TheScrapper is a versatile web scraping tool designed to extract emails, phone numbers, and social media accounts from websites. You can use the gathered information for various purposes, such as further research or contacting the website's owners.

## Installation & Setup

To get started with TheScrapper, follow these simple installation steps:

1. Clone the repository:

```bash
git clone https://github.com/champmq/TheScrapper.git
```

2. Change the directory:

```bash
cd TheScrapper
```

3. Install all the requirements:

```bash
pip3 install -r requirements.txt
```

## Usage

TheScrapper offers several usage options:

- Simple scan:

```bash
python3 TheScrapper.py --url URL
```

- Scan and crawl found URLs:

```bash
python3 TheScrapper.py --url URL --crawl
```

- Retrieve more informaton about found social media accounts:

```bash
python3 TheScrapper.py --url URL -s
```

For additional command-line arguments and options, refer to the help menu:

```bash
python3 TheScrapper.py -h
```

To remove the banner, simply add the "-b" flag.

## Adding More Social Media Sites

If you wish to add more social media sites for scraping. You can do so by appending them to the `socials.txt` file. Feel free to contribute by submtting a pull request if you'd like to share your additions with the community.

## Known Problems

When using a website that is alreadt included in the `socials.txt` file, the `--sm` flag may produce less useful output. To avoid this, consider excluding such URLs or refraining from using the `--sm` flag.

### LICENSE - [GNU](LICENSE)
