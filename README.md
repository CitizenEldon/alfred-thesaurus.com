# 📖 Alfred Thesaurus.com Workflow

A lightning-fast, zero-dependency Alfred Workflow that retrieves synonyms and antonyms natively from [Thesaurus.com](https://www.thesaurus.com).

Designed for writers, developers, and academics who demand instant vocabulary lookups without the start-up lag of heavy third-party frameworks or API rate limits.

![Synonym Search Example](docs/synonym_search.png)

---

## ✨ Key Features

- **Zero External Dependencies:** Built entirely with standard Python 3. It's incredibly lightweight and opens instantly.
- **Smart Auto-Correction:** Accidental typo? The workflow silently catches redirects behind the scenes and intelligently auto-corrects your results, alerting you in the subtitle.
- **Deep Lexical Filtering:** Looking for a specific part of speech? Easily filter results to show strictly nouns or verbs with a simple shortcut key.
- **Configurable Native Settings:** Fully integrates with Alfred 5's Configuration panel, allowing you to remap keywords visually without ever touching a line of code.

<br>

## 🚀 Installation & Setup

1. Download the latest `Thesaurus.alfredworkflow` package from the [Releases](https://github.com/CitizenEldon/alfred-thesaurus.com/releases) page.
2. Double-click the file to install it directly into Alfred. *(Requires Alfred 5+ and Powerpack).*

> [!NOTE] 
> This workflow acts primarily through macOS standard libraries but requires **Python 3**. Python 3 comes pre-installed on modern macOS environments, Xcode Command Line Tools, or via Homebrew.

<br>

## ⚙️ Configuration

You can fully customize the workflow's behavior via Alfred's native User Configuration interface:

![Alfred Configuration](docs/configuration.png)

| Parameter | Default | Description |
| :--- | :--- | :--- |
| **Synonym Trigger** | `syn` | The keyword prefix used to search for synonyms. |
| **Antonyms Trigger** | `ant` | The keyword prefix used to search for antonyms. |
| **Auto-paste** | `Enabled` | When hitting Enter, the workflow instantly pastes the selected word into your active window. |

<br>

## ⌨️ Usage Guide

Trigger the workflow within Alfred using your configured keywords. 

### Core Commands

* **`syn <word>`** : Search for synonyms of a word.
* **`ant <word>`** : Search for antonyms of a word. 
*(Pro-tip: If you're already viewing synonyms, you can quickly append `ant` to the end of your query (e.g., `syn fast ant`) to instantly toggle the list to antonyms).*

![Antonym Search Example](docs/antonym_search.png)

### Part of Speech Filtering

When viewing a large list of synonyms, you can narrow your results down by appending a part-of-speech abbreviation. For example, typing `syn run n` will completely filter the list to only show **noun** forms of "run".

**Supported Filters:**
* `v` (verb)
* `n` (noun)
* `adj` (adjective)
* `adv` (adverb)
* `prep` (preposition)
* `pron` (pronoun)
* `conj` (conjunction)

### Action Modifiers

Hit these modifier keys when pressing `Enter` on a selected result to trigger context actions:
* `Enter` **(↵)** : Copy word to clipboard (and Auto-Paste if configured).
* `Command + Enter` **(⌘↵)** : Open the word directly on Thesaurus.com in your default browser.
* `Shift + Enter` **(⇧↵)** : Navigate deeply! This automatically loops back into Alfred, instantly initiating a brand new search for the highlighted word. 

![Auto-Correction Warning Example](docs/autocorrect_search.png)
*Built-in spelling recovery keeps your research moving rapidly.*

---

## 📜 License & Credits

* Crafted by [Eldon Baines](https://github.com/CitizenEldon).
* Distributed freely under the [MIT License](LICENSE).
* Linguistic data is dynamically parsed from [Thesaurus.com](https://www.thesaurus.com). This is an unofficial plugin and is not directly affiliated with Dictionary.com, LLC.
