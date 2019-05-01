import re
import json


def rtvslo_regex(page):
    output = {}

    output["Author"] = re.search("<div class=\"author-name\">(.*?)</div>", page)[1]
    output["PublishDate"] = re.search("<div class=\"publish-meta\">(\d+\. \w+ \d{4} ob \d{2}:\d{2}).*?</div>", page)[1]
    output["Title"] = re.search("<header class=\"article-header\">.*<h1>(.*)</h1>.*</header>", page)[1]
    output["SubTitle"] = re.search("<div class=\"subtitle\">(.*?)</div>", page)[1]
    output["Lead"] = re.search("<p class=\"lead\">(.*?)</p>", page)[1]

    # content
    # figure = re.search("<div class=\"article-header-media\">.*?<img class=\"image-original loaded\" src=\"(.*?)\">.*?"
    #                   "<figcaption itemprop=\"caption description\">.*</span>(.*?)</figcaption></figure></div>", page)
    # header_fig = figure[1]
    # header_fig_caption = figure[2]

    output["Content"] = re.search("<article class=\"article\">.*?</figure>(.*)<div class=\"gallery\">.*</div></article>", page)[1]
    output["Content"] = re.sub("<script.*?</script>", "", output["Content"])
    output["Content"] = re.sub("<.*?>", "", output["Content"])

    return json.dumps(output,  ensure_ascii=False)


def stringify_file(path):
    with open("../input/" + path, "r", encoding="utf-8") as content_file:
        content = content_file.read()
    return re.sub(r"\s\s+", "", re.sub(r"\n", "", content))


print(rtvslo_regex(stringify_file("rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html")))