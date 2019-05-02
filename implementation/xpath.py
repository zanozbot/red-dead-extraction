from lxml import html
import json


def rtvslo(root):
    output = {}

    output["Author"] = root.xpath("//div[contains(@class, 'author-name')]")[0].text
    output["PublishedTime"] = root.xpath("//div[contains(@class, 'publish-meta')]")[0].text.strip()
    output["Title"] = root.xpath("//h1")[0].text
    output["SubTitle"] = root.xpath("//div[contains(@class, 'subtitle')]")[0].text
    output["Lead"] = root.xpath("//p[contains(@class, 'lead')]")[0].text
    content = root.xpath("//article[contains(@class, 'article')]//p")
    output["Content"] = ""
    for c in content:
        if c.text is not None:
            output["Content"] += c.text

    return json.dumps(output,  ensure_ascii=False)


def get_root(path):
    with open("../input/" + path, "r", encoding="utf-8", errors="ignore") as content_file:
        content = content_file.read()
    return html.fromstring(content)


print(rtvslo(get_root("rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html")))