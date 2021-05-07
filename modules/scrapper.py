from typing import Any
import requests
from requests.models import Response
from bs4 import BeautifulSoup


class Scrapper:
    """
    Scrapper Class
    """
    def __init__(self, urls: object = None, contents: list = []) -> None:
        """Contructor

        Args:
            urls (object, optional): [description]. Defaults to None.
            contents (list, optional): [description]. Defaults to [].
        """

        self.urls = urls

        if urls is not None:
            if self.urls[0][-1] != "/":
                self.urls[0] = str(self.urls[0]).removesuffix("/")

        self.contents = contents

    def clean(self) -> list:
        """clean function

        Returns:
            list: [description]
        """

        contents: list = []

        for content in self.contents:
            soup: any = BeautifulSoup(content, "html.parser")

            for script in soup(["script", "style"]):
                script.extract()

            cleaned: object = soup.get_text()
            lines: object = (line.strip() for line in cleaned.splitlines())
            chunks: object = (phrase.strip() for line in lines for phrase in line.split("  "))
            contents.append('\n'.join(chunk for chunk in chunks if chunk))

        return contents

    def getURLs(self) -> list:
        """getURLs function

        Returns:
            list: [description]
        """
        
        urls: list = []

        for content in self.contents:
            soup = BeautifulSoup(content, "html.parser")

            for link in soup.find_all('a'):
                if link.get("href") is not None:
                    if self.urls[0] not in link.get("href"):
                        if "http" not in link.get("href") and "https" not in link.get("href") and "mailto:" not in link.get("href"):
                            urls.append(self.urls[0] + link.get('href'))
                            continue

                urls.append(link.get("href"))

        return urls

    def getText(self) -> list:
        """getText function

        Returns:
            list: [description]
        """

        contents: list = []

        for url in self.urls:
            req: Response = requests.get(url)
            contents.append(req.text)

        contents = Scrapper(contents=contents).clean()

        return contents
