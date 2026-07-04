import os, re, datetime

# Stellt sicher, dass der Ordner existiert
os.makedirs('content/rezepte', exist_ok=True)

# Liest deine rohen Rezepte
with open('rezepte_roh.txt', 'r', encoding='utf-8') as f:
    content = f.read()

recipes = content.split('---')
date_today = datetime.date.today().isoformat()

# Das Lexikon: Hier weisen wir den Rezepten ihre Tags zu
tag_map = {
    "Butterweicher Konfetti-Rahmspitzkohl mit Apfel": '["Spitzkohl", "Apfel", "Vegetarisch", "Brei-Alternative"]',
    "Energie-Polenta-Schnitten (Großproduktion)": '["Polenta", "Käse", "Fingerfood", "Vorrat"]',
    "Goldene Butter-Gnocchi mit süßem Apfel-Fenchel": '["Gnocchi", "Fenchel", "Apfel", "Vegetarisch"]',
    "Samtiger TK-Brokkoli-Dip": '["Brokkoli", "Dip", "Schnell", "Vegetarisch"]',
    "Magische weiße Blumenkohl-Käse-Creme": '["Blumenkohl", "Käse", "Dip", "Soße"]',
    "Butter-Blumenkohl-Wölkchen am Stiel": '["Blumenkohl", "Fingerfood", "Snack"]',
    "Herzhafte Zucchini-Käse-Waffeln (Grundrezept)": '["Zucchini", "Käse", "Waffeln", "Fingerfood"]',
    "Energie-Polenta-Schnitten (Kleine Portion)": '["Polenta", "Käse", "Fingerfood", "Schnell"]',
    "Saftige Hafer-Bananen-Taler (Mandelmehl-Version)": '["Hafer", "Banane", "Fingerfood", "Süß", "Snack"]'
}

for recipe in recipes:
    recipe = recipe.strip()
    if not recipe: continue
    
    # Sucht die Überschrift (## Titel)
    match = re.search(r'^##\s+(.*)', recipe, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        
        # Baut einen sauberen Dateinamen
        filename = title.lower().replace(' ', '-').replace('ä','ae').replace('ö','oe').replace('ü','ue').replace('ß','ss')
        filename = re.sub(r'[^a-z0-9\-]', '', filename) + '.md'
        
        # Holt sich die passenden Tags aus dem Lexikon (Fallback: Unsortiert)
        tags = tag_map.get(title, '["Unsortiert"]')
        
        # Baut das Hugo Front Matter (TOML Format) mit Tags
        front_matter = f"+++\ntitle = \"{title}\"\ndate = \"{date_today}\"\ndraft = false\ntags = {tags}\n+++\n\n"
        
        # Schreibt die neue Datei direkt in content/rezepte/
        with open(os.path.join('content', 'rezepte', filename), 'w', encoding='utf-8') as out:
            # Entfernt das '## ' aus dem Text
            clean_recipe = re.sub(r'^##\s+.*?\n', '', recipe, flags=re.MULTILINE).strip()
            out.write(front_matter + clean_recipe)

print("Löppt! Alle Rezepte sind getaggt und sauber verpackt.")
