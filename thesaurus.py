import urllib.request
import urllib.parse
from html.parser import HTMLParser
import sys
import json
import re
import os

class ThesaurusParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.synonyms = []
        self.antonyms = []
        self.current_pos = "unknown"
        self.parsing_antonyms = False
        
        self.in_word_link = False
        self.current_word = ""

        self.did_you_mean = None
        self.in_did_you_mean = False
        self.in_spell_suggestion_link = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        href = attrs_dict.get('href', '')
        
        # Check for regular synonyms/antonyms
        if tag == 'a' and href.startswith('https://www.thesaurus.com/browse/'):
            # Some links have "?s=t" trailing, we can ignore that part
            self.in_word_link = True
            self.current_word = ""
            
        elif tag == 'a' and href.startswith('/misspelling?'):
            # Sometimes misspellings redirect or show links
            self.in_spell_suggestion_link = True
            self.current_word = ""

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return

        text_lower = text.lower()

        # Update state
        if text_lower in ['adjective', 'noun', 'verb', 'adverb', 'pronoun', 'preposition', 'conjunction']:
            self.current_pos = text_lower
            self.parsing_antonyms = False
        elif text_lower == 'synonyms':
            self.parsing_antonyms = False
        elif text_lower == 'antonyms':
            self.parsing_antonyms = True
        elif text_lower == 'did you mean?':
            self.in_did_you_mean = True

        if self.in_word_link:
            self.current_word += text

        if self.in_spell_suggestion_link:
            self.current_word += text

    def handle_endtag(self, tag):
        if tag == 'a':
            if self.in_word_link:
                word = self.current_word.strip()
                if word:
                    # Ignore the searched word itself if it accidentally linked
                    entry = {"word": word, "pos": self.current_pos}
                    if self.parsing_antonyms:
                        self.antonyms.append(entry)
                    else:
                        self.synonyms.append(entry)
                self.in_word_link = False
            
            if self.in_spell_suggestion_link:
                if self.current_word and not self.did_you_mean:
                    self.did_you_mean = self.current_word.strip()
                self.in_spell_suggestion_link = False

def search_thesaurus(query):
    # Parse query to see if it has a POS filter
    parts = query.lower().split()
    if not parts:
        return {"items": [{"title": "Type a word to find synonyms...", "valid": False}]}
        
    word = parts[0]
    pos_filter = None
    if len(parts) > 1:
        # Check if the last part is a POS shortcut
        shortcuts = {
            'n': 'noun',
            'v': 'verb',
            'adj': 'adjective',
            'adv': 'adverb',
            'pron': 'pronoun',
            'prep': 'preposition',
            'conj': 'conjunction'
        }
        if parts[-1] in shortcuts:
            pos_filter = shortcuts[parts[-1]]
            word = " ".join(parts[:-1]) # Rejoin the rest
        else:
            word = " ".join(parts) # The whole thing is the word

    search_type = os.environ.get('SEARCH_TYPE', 'synonyms')
    
    url = f"https://www.thesaurus.com/browse/{urllib.parse.quote(word)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    
    redirected_word = None
    try:
        with urllib.request.urlopen(req) as resp:
            # We follow redirects automatically via urllib
            html = resp.read().decode('utf-8')
            final_url = resp.geturl()
            # If the final url is slightly different (e.g. redirected from misspelled to correct)
            # we can extract the redirected word
            match = re.search(r'/browse/([^/]+)', final_url)
            if match:
                word_from_url = urllib.parse.unquote(match.group(1)).split('?')[0]
                if word_from_url.lower() != word.lower():
                    redirected_word = word_from_url
    except Exception as e:
        # HTTP Error usually means 404 Not Found
        html = ""

    parser = ThesaurusParser()
    if html:
        parser.feed(html)

    # Prepare Alfred Items
    items = []
        
    target_list = parser.antonyms if search_type == 'antonyms' else parser.synonyms
    
    # Seen words to prevent duplicates from different contexts being shown repeatedly
    # Although sometimes a word is both a noun and verb. We can group POS.
    word_to_pos = {}
    for item in target_list:
        w = item['word']
        p = item['pos']
        # Filter by POS if requested
        if pos_filter and p != pos_filter:
            continue
        
        if w not in word_to_pos:
            word_to_pos[w] = []
        if p not in word_to_pos[w]:
            word_to_pos[w].append(p)

    is_first_item = True
    for w, pos_list in word_to_pos.items():
        subtitle = ", ".join(pos_list) if pos_list and pos_list != ["unknown"] else "synonym"
        if search_type == 'antonyms':
            subtitle = subtitle.replace("synonym", "antonym")
            
        if redirected_word and is_first_item:
            subtitle += f" (auto-corrected to '{redirected_word}')"
            is_first_item = False
            
        items.append({
            "title": w,
            "subtitle": subtitle,
            "arg": w, # Word passed to next action
            "mods": {
                "cmd": {
                    "valid": True,
                    "arg": f"https://www.thesaurus.com/browse/{urllib.parse.quote(w)}",
                    "subtitle": "Open this word in Thesaurus.com"
                },
                "shift": {
                    "valid": True,
                    "arg": w,
                    "subtitle": f"Search for {'antonyms' if search_type == 'antonyms' else 'synonyms'} of '{w}'"
                }
            }
        })

    if not items:
        if parser.did_you_mean:
            items.append({
                "title": f"Did you mean: {parser.did_you_mean}?",
                "subtitle": "Press enter to search",
                "arg": parser.did_you_mean,
                "variables": {"did_you_mean": "true"}
            })
        else:
            items.append({
                "title": f"No {search_type} found for '{word}'",
                "subtitle": "Please try another word.",
                "valid": False
            })

    # Sort results alphabetically for consistency, or leave them in order of relevance from the site?
    # Thesaurus.com orders by relevance (strongest matches first). Let's maintain their order!
    
    print(json.dumps({"items": items}))

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    search_thesaurus(query)
