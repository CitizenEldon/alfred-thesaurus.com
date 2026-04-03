# Alfred Thesaurus.com Workflow

A fast, zero-dependency Alfred Workflow that retrieves synonyms and antonyms directly from [Thesaurus.com](https://www.thesaurus.com/).

![Icon](icon.png)

## Features

- **No API limits or keys required**: Parses Thesaurus.com seamlessly.
- **Lightning Fast**: Built entirely in Python 3 with no external dependencies (e.g. `requests` or `BeautifulSoup`), ensuring zero start-up lag.
- **Part of Speech Filtering**: Filter results down to just the noun, verb, or adjective you are looking for.
- **Antonyms**: Easily search for antonyms.

## Installation

1. Go to the [Releases](https://github.com/CitizenEldon/alfred-thesaurus.com/releases) page.
2. Download the latest `Thesaurus.alfredworkflow` file.
3. Double-click to install it in Alfred.

*Note: You must have `python3` installed on your Mac. If you are using macOS 12.3 or later, running this workflow will prompt you to install the Xcode Command Line Tools if you don't already have them.*

## Usage

### Basic Search
- Type `syn {word}` to search for synonyms.
- Type `ant {word}` (or `syn {word} ant`) to search for antonyms.

### Modifiers
- `Enter` ↵ : Copies the selected word to your clipboard and pastes it into the frontmost app automatically.
- `Cmd + Enter` ⌘↵ : Opens the selected word directly on Thesaurus.com in your default browser.
- `Shift + Enter` ⇧↵ : Jumps down the rabbit hole and instantly searches Alfred for synonyms/antonyms of the selected word.

### Filtering by Part of Speech
You can narrow down your results by appending a part-of-speech shortcut. 

For example, typing `syn run n` will only show **noun** synonyms of "run".

**Supported Shortcuts:**
- `v` : verb
- `n` : noun
- `adj` : adjective
- `adv` : adverb
- `prep` : preposition
- `pron` : pronoun
- `conj` : conjunction

## Credits
Icon from Thesaurus.com. All data is retrieved from [Thesaurus.com](https://www.thesaurus.com/). This is an unofficial, open-source workflow and is not affiliated with Dictionary.com, LLC.
