from lxml import html
import json
import re


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


def overstock(root):
    output = {}

    items = root.xpath("//table[2]/tbody/tr/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor]/td[2]")
    for i in range(len(items)):
        item = items[i]
        jewel = {}
        jewel["Title"] = item.xpath("./a/b")[0].text
        prices = item.xpath("./table/tbody/tr/td[1]/table/tbody")[0]
        jewel["ListPrice"] = prices.xpath("./tr[1]/td[2]/s")[0].text
        jewel["Price"] = prices.xpath("./tr[2]/td[2]/span/b")[0].text
        saves = re.search("(\$.*?) \((.*?)\)", prices.xpath("./tr[3]/td[2]/span")[0].text)
        jewel["Saving"] = saves[1]
        jewel["SavingPercent"] = saves[2]
        jewel["Content"] = item.xpath("./table/tbody/tr/td[2]/span")[0].text.replace("\n", "").strip()
        output["Jewel"+str(i)] = jewel

    return json.dumps(output, ensure_ascii=False)


def mimovrste(root):
    output = {}

    output["Title"] = root.xpath("//h1")[0].text
    output["Rating"] = root.xpath("//span[contains(@class, 'rat--medium')]/span[1]")[0].text
    energy_level = root.xpath("//span[contains(@class, 'label--energy')]")
    if len(energy_level) > 0:
        output["EnergyLevel"] = energy_level[0].text
    output["Brand"] = root.xpath("//span[contains(@class, 'brand-info')]/a")[0].text
    output["CatalogNumber"] = root.xpath("//span[contains(@class, 'catalog-number')]/span")[0].text
    stickers = root.xpath("//p[contains(@class, 'pro-stickers')]/em")
    output["Stickers"] = []
    for sticker in stickers:
        output["Stickers"].append(sticker.text)
    output["Description"] = root.xpath("//p[contains(@class, 'pro-description--short')]//text()")
    output["Description"] = [e.strip() for e in output["Description"]]
    output["Description"] = " ".join(output["Description"])
    output["Price"] = root.xpath("//b[contains(@class, 'pro-price')]")[0].text.strip()
    output["BasePrice"] = root.xpath("//span[contains(@class, 'base-price')]/del")[0].text
    output["SavingPercent"] = root.xpath("//span[contains(@class, 'base-price')]/span[2]")[0].text.replace("(", "").replace(")", "")
    output["Availability"] = root.xpath("//a[contains(@class, 'con-text--availability')]")[0].text.replace("\n", "").strip()
    output["MarketplacePartner"] = root.xpath("//span[contains(@class, 'marketplace-partner__name')]/b")[0].text
    last_piece = root.xpath("//em[contains(@class, 'label--last-piece')]")
    if len(last_piece) > 0:
        output["LastPiece"] = last_piece[0].text

    return json.dumps(output, ensure_ascii=False)


def get_root(path):
    with open("../input/" + path, "r", encoding="utf-8", errors="ignore") as content_file:
        content = content_file.read()
    return html.fromstring(content)


# print(rtvslo(get_root("rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html")))
# print(overstock(get_root("overstock.com/jewelry02.html")))
# print(mimovrste(get_root("mimovrste.com/item02.html")))
