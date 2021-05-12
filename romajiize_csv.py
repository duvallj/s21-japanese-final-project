import csv
import pykakasi
from jamdict import Jamdict

def get_hepburn(word, kks):
    return kks.convert(word)[0]['hepburn']

def get_translation(word, jd):
    dict_entry = jd.lookup(word).entries
    if len(dict_entry) >= 1:
        gloss = dict_entry[0].senses[0].gloss
        return '/'.join([x.text for x in gloss])
    else:
        return "NOTFOUND"

def get_part_of_speech(word, jd):
    is_noun, is_verb, is_adj, is_adv = False, False, False, False

    dict_entry = jd.lookup(word).entries
    if len(dict_entry) >= 1:
        pos_list = dict_entry[0].senses[0].pos
        for pos in pos_list:
            is_noun = is_noun or ("noun" in pos)
            is_verb = is_verb or ("verb" in pos and not "adv" in pos)
            is_adj = is_adj or ("adj" in pos)
            is_adv = is_adv or ("adv" in pos)

    return is_noun, is_verb, is_adj, is_adv



def romajiize_csv(filename, kks, jd):
    output_filename = 'romaji_' + filename

    file = open(filename, 'r', encoding='utf-8')
    output_file = open(output_filename, 'w', encoding='utf-8', newline='')

    reader = csv.DictReader(file)
    writer = csv.DictWriter(
        output_file,
        ['Hepburn', 'Kana', 'English',\
         'Is Noun', 'Is Verb', 'Is Adjective', 'Is Adverb',\
         'Frequency']
    )
    writer.writeheader()

    for row in reader:
        word = row['Item']
        hepburn = get_hepburn(word, kks)
        english = get_translation(word, jd)
        is_noun, is_verb, is_adj, is_adv = get_part_of_speech(word, jd)
        writer.writerow({
            'Hepburn': hepburn,
            'Kana': word,
            'English': english,
            'Is Noun': is_noun,
            'Is Verb': is_verb,
            'Is Adjective': is_adj,
            'Is Adverb': is_adv,
            'Frequency': row['Frequency']
        })

    file.close()
    output_file.close()

if __name__ == '__main__':
    import os
    files = os.listdir(os.getcwd())
    kks = pykakasi.kakasi()
    jd = Jamdict()

    for filename in files:
        if filename.endswith('.csv') and not filename.startswith('romaji'):
            print(f"Romaji-izing {filename}")
            romajiize_csv(filename, kks, jd)

    print("Done")
