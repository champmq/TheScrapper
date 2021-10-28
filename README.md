# TheScrapper

Scrape emails, phone numbers and social media accounts from a website. <br>
You can use the found information to gather more information or just find ways to contact the site.

## Installation & Setup

```bash
git clone https://github.com/champmq/TheScrapper.git
cd TheScrapper
pip3 install -r requirements.txt
```
<br>

## Usage
```bash
# Simple scan
python3 TheScrapper.py --url URL
# Use found URLS and scan them too
python3 TheScrapper.py --url URL --crawl
# Get more info about the found socialmedia accounts
python3 TheScrapper.py --url URL -s
# There are some more args just use:
python3 TheScrapper.py -h
```
*If you dont like the banner just add "-b".*
<br>

## SocialMedia
If you want to add more SocialMedia sites just append them to the [`socials.txt`](./socials.txt) file and if you want, you can add them with a [pull request](https://www.lifewire.com/best-products-4781319).

## TODO
 - [ ] Verbose Mode
 - [ ] API

# Bugs or ideas?
If you find any bug or if you have some ideas create an [issue](https://github.com/champmq/TheScrapper/issues).
