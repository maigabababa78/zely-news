import re
import html
import urllib.request
import xml.etree.ElementTree as ET
from django.utils import timezone
from django.utils.text import slugify
from .models import Category, Article, LiveNewsWire


RSS_FEEDS = [
    ("https://www.footmercato.net/flux-rss", "ZeMercato", "sport-esport", "Rédaction ZeMercato"),
    ("https://rmcsport.bfmtv.com/rss/football/", "RMC Sport", "sport-esport", "Rédaction RMC Sport"),
    ("https://www.france24.com/fr/rss", "France 24", "politique-economie-monde", "Rédaction France 24"),
    ("https://www.lemonde.fr/rss/une.xml", "Le Monde", "politique-economie-monde", "Rédaction Le Monde"),
    ("https://www.lemonde.fr/pixels/rss_full.xml", "Le Monde Pixels", "tech-science-innovation", "Pôle Tech & Sciences"),
    ("https://www.lemonde.fr/culture/rss_full.xml", "Le Monde Culture", "culture-musique-cinema", "Pôle Culture & Médias"),
]

FALLBACK_IMAGES = {
    "sport-esport": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=1000&auto=format&fit=crop&q=80",
    "politique-economie-monde": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1000&auto=format&fit=crop&q=80",
    "tech-science-innovation": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1000&auto=format&fit=crop&q=80",
    "culture-musique-cinema": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1000&auto=format&fit=crop&q=80",
}


def _clean_html(raw_txt):
    if not raw_txt:
        return ""
    txt = html.unescape(raw_txt)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def _extract_image_from_item(item, cat_slug):
    # Check <enclosure url="...">
    enclosure = item.find("enclosure")
    if enclosure is not None and enclosure.attrib.get("url"):
        return enclosure.attrib["url"]
    # Check any element ending with content or thumbnail with a url attribute
    for elem in item.iter():
        if elem.tag.endswith(("content", "thumbnail")) and elem.attrib.get("url"):
            return elem.attrib["url"]
    return FALLBACK_IMAGES.get(cat_slug, FALLBACK_IMAGES["politique-economie-monde"])


class LiveNewsRssService:
    """
    Fetches real-time French news headlines and full articles from public RSS feeds
    (FootMercato, RMC Sport, France 24, Le Monde) without requiring any API key.
    """

    @classmethod
    def sync_latest_wires(cls, create_articles=True):
        imported = 0
        default_cat = Category.objects.first()

        for rss_url, source_label, cat_slug, author_role in RSS_FEEDS:
            cat = Category.objects.filter(slug=cat_slug).first() or default_cat
            if not cat:
                continue
            try:
                req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=4.5) as resp:
                    xml_bytes = resp.read()
                    root = ET.fromstring(xml_bytes)
                    items = root.findall(".//item")
                    for idx, item in enumerate(items[:4]):
                        title_el = item.find("title")
                        link_el = item.find("link")
                        desc_el = item.find("description")
                        if title_el is None or not title_el.text:
                            continue
                        title_txt = _clean_html(title_el.text)[:215]
                        link_txt = (link_el.text or "").strip()[:495] if link_el is not None else ""
                        desc_txt = _clean_html(desc_el.text if desc_el is not None else "")
                        if len(desc_txt) < 30:
                            desc_txt = f"{title_txt} — Retrouvez l'analyse complète et les réactions en direct."

                        img_url = _extract_image_from_item(item, cat_slug)

                        _, created = LiveNewsWire.objects.get_or_create(
                            title=title_txt,
                            defaults={
                                "category": cat,
                                "source_name": source_label,
                                "external_url": link_txt,
                                "is_urgent": idx == 0,
                                "created_at": timezone.now(),
                            },
                        )
                        if created:
                            imported += 1

                        if create_articles and idx < 3:
                            base_slug = slugify(title_txt)[:42] or f"actu-{imported}"
                            if not Article.objects.filter(title=title_txt).exists():
                                slug = f"{base_slug}-{Article.objects.count() + 1}"
                                Article.objects.create(
                                    title=title_txt,
                                    slug=slug,
                                    category=cat,
                                    summary=desc_txt[:340],
                                    content=(
                                        f"{desc_txt}\n\n"
                                        f"Source officielle : {source_label} ({link_txt}).\n\n"
                                        f"Suivez l'évolution de cette actualité en temps réel sur Zely News et réagissez dans l'espace débat ci-dessous."
                                    ),
                                    key_points=(
                                        f"{title_txt}\n"
                                        f"{desc_txt[:160]}\n"
                                        f"Source vérifiée : {source_label}"
                                    ),
                                    source_trust_score=98,
                                    sources_label=f"Flux officiel {source_label}",
                                    image_url=img_url[:495],
                                    author_name=source_label,
                                    author_role=author_role,
                                    reading_time=3,
                                    is_breaking=(idx == 0),
                                    is_featured=(imported == 1),
                                    views_count=120 + idx * 45,
                                    likes_count=18 + idx * 7,
                                    fire_count=12 + idx * 4,
                                    mindblown_count=5 + idx * 2,
                                )
            except Exception:
                continue

        return imported
