import re
import string


class InfoReader:
    def __init__(self, content=None, social_path="./socials.txt"):
        if content is None:
            content = {
                "text": [],
                "urls": []
            }
        self.content = content
        self.social_path = social_path

    def getPhoneNumber(self):
        # Doesnt work that good
        numbers = []
        texts = self.content["text"]
        for text in texts:
            for n in text.split("\n"):
                if re.match("[0-9 /()+]", n):
                    for letter in string.ascii_letters:
                        n = n.replace(letter, "")
                    numbers.append(n)
        return list(dict.fromkeys(numbers))

    def getEmails(self):
        emails = []
        texts = self.content["text"]
        for text in texts:
            for s in text.split("\n"):
                if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", s):
                    emails.append(s)

        for link in self.content["urls"]:
            if "mailto:" in link:
                emails.append(link.replace("mailto:", ""))
        return list(dict.fromkeys(emails))

    def getSocials(self):
        sm_accounts = []
        socials = open(self.social_path, "r+").readlines()
        for url in self.content["urls"]:
            for s in socials:
                if s.replace("\n", "").lower() in url.lower():
                    sm_accounts.append(url)
        return list(dict.fromkeys(sm_accounts))
