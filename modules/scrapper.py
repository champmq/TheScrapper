import requests
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self, urls=None, contents=[]):
        self.urls = urls
        if urls is not None:
            if self.urls[0][-1] != "/":
                self.urls[0] = str(self.urls[0]).removesuffix("/")
        self.contents = contents

    def clean(self):
        contents = []
        for content in self.contents:
            soup = BeautifulSoup(content, "html.parser")
            for script in soup(["script", "style"]):
                script.extract()
            cleaned = soup.get_text()
            lines = (line.strip() for line in cleaned.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            contents.append('\n'.join(chunk for chunk in chunks if chunk))
        return contents

    def getURLs(self):
        urls = []
        for content in self.contents:
            soup = BeautifulSoup(content, "html.parser")
            for link in soup.find_all('a'):
                if link.get("href") is not None:
                    if self.urls[0] not in link.get("href"):
                        if "http" not in link.get("href") and "https" not in link.get("href") and "mailto:" not in link.get("href"):
                            urls.append(self.urls[0] + link.get('href'))
                            continue
                urls.append(link.get("href"))
        return list(dict.fromkeys(urls))

    def getText(self):
        contents = []
        for url in self.urls:
            req = requests.get(url)
            contents.append(req.text)
        contents = Scrapper(contents=contents).clean()
        return contents
