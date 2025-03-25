from english_words import get_english_words_set
import pyperclip

word_list = list(get_english_words_set(['web2'], lower=True))
s = input('Enter all letters in bee:')
while not (s and len(s) == 7 and len(set(s)) == len(s)):
    s = input('Must be 7 unique letters, try again:')

c = input('Enter center letter:')
while not (c and len(c) == 1 and c in s):
    s = input(f'Must be a single letter in ${c}, try again:')

res = set()
for word in word_list:
    if len(word) < 4:
        continue
    chars = set(word)
    if c not in chars:
        continue
    for char in chars:
        if char not in s:
            break
    else:
        res.add(word)

word_candidates = list(res)
word_candidates.sort()

formatted = ', '.join(f'"{word}"' for word in word_candidates)
jslist = f"words = [{formatted}]\n"

jsscript = """
found_words = Array.from(document.querySelectorAll('.sb-anagram')).map(el => el.textContent);
words = words.filter((word) => !found_words.has(word))
async function typeWords() {
    const enterKeyUp = new KeyboardEvent('keyup', {
        bubbles: true,
        cancelable: true,
        key: 'Enter',
        keyCode: 13,
        code: 'Enter'
    });
    const enterKeyDown = new KeyboardEvent('keydown', {
        bubbles: true,
        cancelable: true,
        key: 'Enter',
        keyCode: 13,
        code: 'Enter'
    });
    
    for (let word of words) {
        for (let char of word) {
            let keyDownEvent = new KeyboardEvent('keydown', {
                bubbles: true,
                cancelable: true,
                key: char,
                keyCode: char.toUpperCase().charCodeAt(0),
                code: `Key${char.toUpperCase()}`
            });

            let keyUpEvent = new KeyboardEvent('keyup', {
                bubbles: true,
                cancelable: true,
                key: char,
                keyCode: char.toUpperCase().charCodeAt(0),
                code: `Key${char.toUpperCase()}`
            });

            document.body.dispatchEvent(keyDownEvent);
            document.body.dispatchEvent(keyUpEvent);
        }

        document.body.dispatchEvent(enterKeyDown);
        document.body.dispatchEvent(enterKeyUp);
        
        await new Promise(r => setTimeout(r, $('.error-message') ? 2000 : 100));
    };
}
typeWords();
"""
print(f'All words: ${word_candidates}')
script = jslist + jsscript
pyperclip.copy(jslist + jsscript)
print('Script in clipboard!')
