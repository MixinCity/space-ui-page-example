import json


def main():
    data = json.load(open("src/data.json"))
    html = open("src/index.html").read()

    # meta
    meta = data["page"]["meta"]
    for key in meta:
        val = meta.get(key)
        if val:
            html = html.replace("$" + key + "$", f'"{val}"')
    html = html.replace('<title>"', "<title>").replace('"</title>', "</title>")

    # analytics
    google_tag_id = data["page"].get("analytics", {}).get("google_tag_id")
    if google_tag_id:
        html = insert_google_analytics(google_tag_id, html)

    # output
    with open("public/index.html", "w") as f:
        f.write(html)
    json.dump(data, open("public/data.json", "w"), ensure_ascii=False)


def insert_google_analytics(google_tag_id: str, html: str):
    template = """
<script async src="https://www.googletagmanager.com/gtag/js?id=$google_tag_id$"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', '$google_tag_id$');
</script>"""

    html = html.replace(
        "</head>", template.replace("$google_tag_id$", google_tag_id) + "</head>"
    )
    return html.replace("\n", "")


if __name__ == "__main__":
    main()
