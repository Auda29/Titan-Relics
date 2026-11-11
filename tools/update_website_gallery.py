"""Rebuild both static website galleries from the shared screenshot manifest.

Run from any directory with Python 3. No third-party dependencies required.
"""
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- relic-slideshows:start -->'
END = '<!-- relic-slideshows:end -->'
CONFIG = [
    ('titan-skull', 'Titan Skull', 'TITANENRESTE', 'TITAN REMAINS',
     'Ein gekröntes Haupt, zurückgelassen in der offenen Landschaft. Das Gras wächst längst zwischen den Überresten.',
     'A crowned head, left behind in the open landscape. Grass has long since grown between its remains.',
     '2026-11-11_071851-titan-skull-village-context'),
    ('world-tree', 'World Tree', 'ZUFLUCHT', 'REFUGE',
     'Unter den ausladenden Ästen liegt ein Ort zum Durchatmen. Die Aura des Baums stärkt dich in seiner Nähe.',
     'A place to catch your breath beneath its spreading branches. The tree\'s aura strengthens you nearby.',
     '2026-11-11_072616-world-tree-forest'),
    ('small-colossus', 'Small Colossus', 'VERLASSENE MASCHINEN', 'ABANDONED MACHINES',
     'Der kleinere der beiden Kolosse. Erkunde seine zugänglichen Öffnungen und halte nach brauchbaren Überbleibseln Ausschau.',
     'The smaller of the two colossi. Explore its accessible openings and keep an eye out for useful remains.',
     '2026-11-11_072233-small-colossus-meadow'),
    ('colossus', 'Colossus', 'VERLASSENE MASCHINEN', 'ABANDONED MACHINES',
     'Der große Koloss in unterschiedlichen Landschaften, aus der Nähe und von innen. Folge einer Expeditionskarte zu diesem einzigartigen Ort deiner Welt.',
     'The great Colossus in different landscapes, up close and from inside. Follow an expedition map to this unique site in your world.',
     '2026-11-11_071641-colossus-desert-front'),
    ('obelisk', 'Obelisk', 'ARCHÄOLOGIE', 'ARCHAEOLOGY',
     'Ein weithin sichtbares Zeichen. Nimm einen Pinsel mit und untersuche den verdächtigen Sand und Kies in seinem Umfeld.',
     'A landmark visible from afar. Bring a brush and investigate the suspicious sand and gravel around it.',
     '2026-11-11_071205-obelisk-low-view'),
    ('ruined-tower', 'Ruined Tower', 'VERGESSENE BAUWERKE', 'FORGOTTEN STRUCTURES',
     'Die Mauern stehen noch, doch die Natur hat ihren Platz zurückerobert. Ein weiterer Halt auf deiner Reise durch die Oberwelt.',
     'The walls are still standing, but nature has reclaimed its place. Another stop on your journey through the Overworld.',
     '2026-11-11_072401-ruined-tower-snow'),
    ('sword-skull', 'Sword Skull', 'TITANENRESTE', 'TITAN REMAINS',
     'Eine Klinge ragt aus dem verwitterten Schädel. Entdecke das zweite Schädeldesign bei Tageslicht, über den Badlands und unter dem Sternenhimmel.',
     'A blade rises from the weathered skull. Discover the second skull design in daylight, above the badlands and under a starry sky.',
     '2026-11-11_071733-sword-skull-daylight'),
]
CAPTURES = {
    'de': {'beta-1-playtest': 'Beta-1-Spieltest', 'beta-3-playtest': 'Beta-3-Spieltest', 'development-playtest': 'Entwicklungsspieltest'},
    'en': {'beta-1-playtest': 'Beta 1 playtest', 'beta-3-playtest': 'Beta 3 playtest', 'development-playtest': 'Development playtest'},
}


def render_gallery(images, language):
    en = language == 'en'
    cards = []
    for number, (subject, name, category_de, category_en, text_de, text_en, first) in enumerate(CONFIG, 1):
        slides = [image for image in images if image['subject'] == subject]
        slides.sort(key=lambda image: (image['id'] != first, image['id']))
        if not slides or slides[0]['id'] != first:
            raise ValueError(f'Missing featured screenshot for {subject}')
        links = []
        for index, image in enumerate(slides):
            title = image[f'title_{language}']
            capture = f"{CAPTURES[language][image['capture']]} · {image['date']} · {'With shaders' if en else 'Mit Shadern'}"
            src = 'images/screenshots/' + image['file']
            if not (ROOT / 'docs' / src).is_file():
                raise ValueError(f'Missing image: {src}')
            label = ('Enlarge image: ' if en else 'Bild vergrößern: ') + title
            links.append(f'''<a class="relic-photo slide" data-gallery data-title="{escape(title, quote=True)}" data-capture="{escape(capture, quote=True)}" href="{escape(src, quote=True)}" aria-label="{escape(label, quote=True)}"{' hidden' if index else ''}>
  <img src="{escape(src, quote=True)}" width="960" height="527" loading="lazy" alt="{escape(title, quote=True)}" draggable="false"><span class="expand" aria-hidden="true">↗</span>
</a>''')
        first_image = slides[0]
        caption = f"{first_image[f'title_{language}']} · {CAPTURES[language][first_image['capture']]} · {first_image['date']}"
        previous, following = ('Previous image', 'Next image') if en else ('Vorheriges Bild', 'Nächstes Bild')
        play = 'Play slideshow' if en else 'Slideshow abspielen'
        cards.append(f'''<article class="relic slideshow" data-slideshow="{subject}" role="region" aria-roledescription="{'carousel' if en else 'Bilderkarussell'}" aria-labelledby="relic-{subject}">
  <div class="slideshow-viewport">{''.join(links)}</div>
  <div class="slideshow-controls" hidden>
    <button type="button" data-slide-prev aria-label="{previous}">←</button>
    <span class="slide-count" aria-label="{'Image count' if en else 'Bildzähler'}">1 / {len(slides)}</span>
    <button type="button" class="slide-play" data-slide-play aria-label="{play}" aria-pressed="false"><span data-play-icon aria-hidden="true">▶</span> <span data-play-label>{'Play' if en else 'Abspielen'}</span></button>
    <button type="button" data-slide-next aria-label="{following}">→</button>
  </div>
  <p class="slide-caption" aria-live="polite" aria-atomic="true">{escape(caption)}</p>
  <div class="relic-label"><h3 id="relic-{subject}">{name}</h3><span>{number:02d} / {category_en if en else category_de}</span></div>
  <p>{text_en if en else text_de}</p>
  <noscript><p><a href="https://github.com/Auda29/Titan-Relics/blob/main/docs/images/screenshots/README.md">{'All photos in the screenshot library' if en else 'Alle Fotos in der Screenshot-Sammlung'} ↗</a></p></noscript>
</article>''')
    intro = ('Browse each relic with the arrows or swipe its image. Select Play to cycle through its photos. Click an image to enlarge it.' if en else 'Blättere mit den Pfeilen oder wische über das Bild. Mit Abspielen läuft die Slideshow. Ein Klick auf das Bild öffnet die Großansicht.')
    return START + '\n<p class="gallery-help">' + intro + '</p>\n<div class="gallery">\n' + '\n'.join(cards) + '\n</div>\n' + END


def main():
    images = json.loads((ROOT / 'docs/images/screenshots/manifest.json').read_text())['images']
    subjects = {config[0] for config in CONFIG}
    if any(image['subject'] not in subjects for image in images):
        raise ValueError('Unknown screenshot subject')
    for language, filename in [('de', 'index.html'), ('en', 'en.html')]:
        path = ROOT / 'docs' / filename
        text = path.read_text()
        pattern = re.escape(START) + r'.*?' + re.escape(END)
        text, count = re.subn(pattern, lambda _: render_gallery(images, language), text, flags=re.DOTALL)
        if count != 1:
            raise ValueError(f'Expected one gallery marker pair in {filename}, found {count}')
        path.write_text(text)
        print(f'{filename}: {len(images)} images across {len(CONFIG)} relic slideshows')


if __name__ == '__main__':
    main()
