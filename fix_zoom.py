import re

with open('css/style.css', 'r') as f:
    css = f.read()

# Fix hero-mockup CSS
hero_mockup_new = """
.hero-mockup {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
    transform: none;
}
.hero-mockup img {
    width: 100%;
    height: auto;
    display: block;
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.hero-mockup:hover img {
    transform: scale(1.06);
}
"""

css = re.sub(r'\.hero-mockup\s*{[^}]*}', '', css)
css = re.sub(r'\.hero-mockup:hover\s*{[^}]*}', '', css)

# Fix showcase-image CSS
showcase_new = """
.showcase-image {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}
.showcase-image img {
    width: 100%;
    height: auto;
    display: block;
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    border-radius: 0;
    box-shadow: none;
}
.showcase-image:hover img {
    transform: scale(1.06);
}
"""

css = re.sub(r'\.showcase-image\s*{[^}]*}', '', css)
css = re.sub(r'\.showcase-image img\s*{[^}]*}', '', css)
css = re.sub(r'\.showcase-image img:hover\s*{[^}]*}', '', css)

# Append the new rules at the end of the file (before the responsive queries or just at the end)
# Actually, appending at the end might override media queries, let's just put it where hero-screen is.
# Wait, just appending before the media queries is best.
media_query_index = css.find('@media')
if media_query_index != -1:
    css = css[:media_query_index] + hero_mockup_new + showcase_new + css[media_query_index:]
else:
    css += hero_mockup_new + showcase_new

with open('css/style.css', 'w') as f:
    f.write(css)
print("CSS updated successfully")
