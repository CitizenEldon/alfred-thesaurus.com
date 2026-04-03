"""
Alfred Workflow: Thesaurus.com Integration

A dependency-free HTML-parsing script built exclusively with standard Python 3.
It queries Thesaurus.com, parses the DOM natively, categorizes results by 
part of speech, handles basic spelling auto-correction via redirects, and 
structures the output into a JSON format digestible by Alfred 5.

Usage: 
    python3 thesaurus.py "<query>"
"""

import urllib.request
import urllib.parse
from html.parser import HTMLParser
import sys
import json
import re
import os

class ThesaurusParser(HTMLParser):
    """
    A lightweight, native HTML parser designed to stream Thesaurus.com 
    source code and extract grouped synonyms and antonyms without 
    loading heavy DOM-tree structures into memory.
    """
    
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
        """Intercept anchors to isolate vocabulary links and spelling suggestions."""
        attrs_dict = dict(attrs)
        href = attrs_dict.get('href', '')
        
        if tag == 'a' and href.startswith('https://www.thesaurus.com/browse/'):
            self.in_word_link = True
            self.current_word = ""
            
        elif tag == 'a' and href.startswith('/misspelling?'):
            self.in_spell_suggestion_link = True
            self.current_word = ""

    def handle_data(self, data):
        """Monitor text nodes to track the active lexical category and data extraction state."""
        text = data.strip()
        if not text:
            return

        text_lower = text.lower()

        # Track the active Part of Speech header dominating the current HTML block
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
        """Finalize state and commit the aggregated word to the memory stack."""
        if tag == 'a':
            if self.in_word_link:
                word = self.current_word.strip()
                if word:
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
    """
    Executes a lexical query against Thesaurus.com, formats the results against 
    active filters, and outputs Alfred-compliant JSON.
    """
    parts = query.lower().split()
    if not parts:
        return {"items": [{"title": "Type a word to find synonyms...", "valid": False}]}
        
    word = parts[0]
    pos_filter = None
    
    # Detect standard part-of-speech abbreviations isolated as trailing arguments
    if len(parts) > 1:
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
            word = " ".join(parts[:-1])
        else:
            word = " ".join(parts)

    search_type = os.environ.get('SEARCH_TYPE', 'synonyms')
    url = f"https://www.thesaurus.com/browse/{urllib.parse.quote(word)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    
    redirected_word = None
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            final_url = resp.geturl()
            
            # Autocorrect detection: if Thesaurus.com 301 redirects to a different word, isolate it
            match = re.search(r'/browse/([^/]+)', final_url)
            if match:
                word_from_url = urllib.parse.unquote(match.group(1)).split('?')[0]
                if word_from_url.lower() != word.lower():
                    redirected_word = word_from_url
    except Exception:
        # 404 Not Found returns gracefully as an empty HTML string
        html = ""

    parser = ThesaurusParser()
    if html:
        parser.feed(html)

    items = []
    target_list = parser.antonyms if search_type == 'antonyms' else parser.synonyms
    
    # Consolidate duplicate words natively tracking multiple parts of speech
    word_to_pos = {}
    for item in target_list:
        w = item['word']
        p = item['pos']
        
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
            "arg": w,
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

    # Render Fallbacks
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

    print(json.dumps({"items": items}))

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    search_thesaurus(query)
