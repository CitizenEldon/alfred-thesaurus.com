# Thesaurus.com Workflow for Alfred

A fast, lightweight Alfred Workflow that natively retrieves synonyms and antonyms directly from [Thesaurus.com](https://www.thesaurus.com/), completely free of charge.

## Overview

Unlike many dictionary workflows, this tool relies entirely on the standard libraries built into macOS. By bypassing heavy external libraries or paid APIs, this workflow parses Thesaurus.com results instantly. You simply type your command, and the workflow does the rest—even natively managing spelling mistakes and auto-correcting your typos under the hood.

![User Configuration Interface](docs/configuration.png)
*You can configure the keyword triggers and auto-pasting behavior directly within Alfred.*

## Features

- **No Third-Party Dependencies:** Built entirely with standard Python 3. This guarantees it opens instantly without the start-up lag associated with heavy external packages.
- **Auto-Correction Built In:** If you accidentally search for a misspelled word (e.g., `heppy`), the workflow gracefully detects the website's redirect and auto-corrects your results to the closest matching word.
- **Part of Speech Subtitles:** Synonyms are deeply categorized. A quick glance at the subtitle will tell you exactly whether a word is acting as a noun, verb, or adjective in that context.
- **Customizable Triggers:** Using Alfred 5's native User Configuration panel, you can remap the `syn` and `ant` keywords to whatever trigger feels most natural to you.
- **Intelligent Antonyms:** Not just restricted to synonyms—invoke the antonyms search directly or append the `ant` flag to effortlessly view opposites.

## Installation

1. Download the latest `Thesaurus.alfredworkflow` from the [Releases](https://github.com/CitizenEldon/alfred-thesaurus.com/releases) page.
2. Double-click the downloaded file to install it directly into Alfred 5.

*Note: Ensure you have `python3` installed on your Mac (standard with the Xcode Command Line Tools or Homebrew).*

## Usage Guide

To begin utilizing the workflow, open your Alfred window and type the default synonym trigger.

### Basic Searching

- Type `syn {word}` to load a list of synonyms.
- Type `ant {word}` to load a list of antonyms.
*(Alternatively, you can instantly search for antonyms by typing `syn {word} ant` without changing your keyword prefix).*

![Basic Search Example](docs/synonym_search.png)
*Typing `syn lull` will reveal a diverse list of categorized nouns and verbs.*

### Modifiers & Shortcuts

Once your list of words appears, you can press various keyboard modifiers to change what happens when you press Enter:
- **Enter (↵)** : Automatically copies the selected synonym directly to your clipboard. If the Auto-Paste configuration is enabled, it instantly pastes the word into whichever app you were typing in.
- **Command + Enter (⌘↵)** : Opens your default web browser and navigates directly to that word's page on Thesaurus.com.
- **Shift + Enter (⇧↵)** : Jumps down the rabbit hole! Instantly clears the search and triggers Alfred again specifically searching for synonyms of the newly selected word.

![Auto-Correction Example](docs/autocorrect_search.png)
*If you misspell a word, the top subtitle clearly indicates what word it automatically corrected your search to!*

### Filtering by Lexical Category

Occasionally, you only want to look at words that match a specific part of speech. You can narrow down your results by simply appending a part-of-speech abbreviation to the end of your query.

**For example**, typing `syn run n` will completely filter the list and only show **noun** synonyms for "run". The workflow supports the following abbreviations:
- `v` : verb
- `n` : noun
- `adj` : adjective
- `adv` : adverb
- `prep` : preposition
- `pron` : pronoun
- `conj` : conjunction

![Antonym Filtering](docs/antonym_search.png)
*Searching for antonyms functions identically to synonyms, maintaining fast and reliable response times.*

## License

This project is open-source and provided freely under the [MIT License](LICENSE). 

## Legal & Credits

All linguistic data is retrieved directly from [Thesaurus.com](https://www.thesaurus.com/). This project is an unofficial workflow designed for convenience and is generally not affiliated with Dictionary.com, LLC.
