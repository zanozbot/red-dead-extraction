import re
import json


def rtvslo_regex(page):
    output = {}

    output["Author"] = re.search("<div class=\"author-name\">(.*?)</div>", page)[1]
    output["PublishDate"] = re.search("<div class=\"publish-meta\">(\d+\. \w+ \d{4} ob \d{2}:\d{2}).*?</div>", page)[1]
    output["Title"] = re.search("<header class=\"article-header\">.*<h1>(.*)</h1>.*</header>", page)[1]
    output["SubTitle"] = re.search("<div class=\"subtitle\">(.*?)</div>", page)[1]
    output["Lead"] = re.search("<p class=\"lead\">(.*?)</p>", page)[1]
    output["Content"] = re.search("<article class=\"article\">.*?</figure>(.*)<div class=\"gallery\">.*</div></article>", page)[1]
    output["Content"] = re.sub("<script.*?</script>", "", output["Content"])
    output["Content"] = re.sub("<.*?>", "", output["Content"])

    return json.dumps(output,  ensure_ascii=False)


def overstock_regex(page):
    output = {}
    page = re.sub("<script.*?</script>", "", page)
    results = re.findall("<td valign=\"top\"> <a href=.*?<b>(.*?)</b></a>.*?"  # Title
                         "<td align=\"left\" nowrap=\"nowrap\"><s>(.*?)</s></td>.*?"  # ListPrice
                         "<span class=\"bigred\"><b>(.*?)</b>.*?"  # Price
                         "<span class=\"littleorange\">(\$.*?) \((.*?)\)</span>.*?"  # Saving, SavingPercent
                         "<span class=\"normal\">(.*?)</span>", page)  # Content

    for i in range(len(results)):
        content = re.sub("<br>.*<b>", " ", results[i][5])
        content = re.sub("</b>", "", content)

        jewel = {}

        jewel["Title"] = results[i][0]
        jewel["ListPrice"] = results[i][1]
        jewel["Price"] = results[i][2]
        jewel["Saving"] = results[i][3]
        jewel["SavingPercent"] = results[i][4]
        jewel["Content"] = content

        output["Jewel"+str(i)] = jewel

    return json.dumps(output, ensure_ascii=False)


def mimovrste_regex(page):
    output = {}

    output["Title"] = re.search("pro-column.*?<h1.*?>(.*?)</h1>", page)[1]
    output["Rating"] = re.search("pro-subtitle-info.*?con-reader\">(.*?)</span>", page)[1]
    energy_level = re.search("Energijska nalepka.*?>(.*?)</span>", page)
    if energy_level is not None:
        output["EnergyLevel"] = energy_level[1]
    output["Brand"] = re.search("brand-info.*?link--pro-subtitle-info\">(.*?)</a>", page)[1]
    output["CatalogNumber"] = re.search("catalog-number\">(.*?)</span>", page)[1]
    output["Stickers"] = re.findall("<em.*?>(.*?)</em>", page)
    output["Description"] = re.search("pro-description.*?>(.*?)</p>", page)[1]
    output["Description"] = re.sub("<.*?>", "", output["Description"])
    output["Price"] = re.search("pro-price .*?>(.*?)</b>", page)[1]
    savings = re.search("base-price.*?<del>(.*?)</del>,(.*?)<span.*?>\((\d{0,3}).*?\)</span>", page)
    output["BasePrice"] = savings[1]
    output["Save"] = savings[2]
    output["SavingPercent"] = savings[3] + "%"
    last_piece = re.search("label--last-piece\">(.*?)</em>", page)
    if last_piece is not None:
        output["LastPiece"] = last_piece[1]
    output["Availability"] = re.search("con-text--availability.*?>(.*?)</a>", page)[1]
    output["MarketplacePartner"] = re.search("marketplace-partner__name.*?<b>(.*?)</b>", page)[1]

    return json.dumps(output, ensure_ascii=False)


def stringify_file(path):
    with open("../input/" + path, "r", encoding="utf-8", errors="ignore") as content_file:
        content = content_file.read()
    return re.sub(r"\s\s+", "", re.sub(r"\n", "", content))


# print(rtvslo_regex(stringify_file("rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html")))
# print(overstock_regex(stringify_file("overstock.com/jewelry02.html")))
# print(mimovrste_regex(stringify_file("mimovrste.com/item01.html")))
