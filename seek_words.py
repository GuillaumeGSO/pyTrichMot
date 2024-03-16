import codecs
import unidecode

def is_list_empty_or_full_of_none(lst):
    if not lst:
        return True
    if all(x is None or not x for x in lst):
        return True
    return False


def is_search_by_content(word, lst_car=[], strict = False):
    """
    Returns False if word is not set
    Returns False if lstCar is empty
    Returns False if less caracters in lstCar than in word
    Returns True if each and every caracters are in lstCar
    """
    if word == None or len(word) == 0:
        return False
    if is_list_empty_or_full_of_none(lst_car):
        return False
    
    word_no_accent = unidecode.unidecode(word).replace("à", "a").replace("é", "e").replace("è", "e").replace("ê", "e").replace("ô", "o")
    
    for car in word_no_accent:
      if car not in lst_car:
        return False
      else:
        if strict:
          lst_car.remove(car)
    return True


def is_search_by_hint(word, hint_list=[]):
    """
    Returns False if word is not provided.
    Returns True if no hints are provided.
    Returns False if the word does not contain the character at the hint position.
    Returns False if the word has the character at the inverted hint position.
    Returns True if the word contains each letter of the hint at the correct position.
    """
    if not word:
        return False
    if is_list_empty_or_full_of_none(hint_list):
        return True
  
    for hint in hint_list:
        if hint['inverted']:
            if word[int(hint['pos'])-1] == hint['car']:
                return False
        else:
            if word[int(hint['pos'])-1] != hint['car']:
                return False
    return True


def search_in_file(lang="fr", nb_car=99, lst_car=[], lst_hint=[], strict= False):
    is_empty_hint = is_list_empty_or_full_of_none(lst_hint)
    is_empty_cars = is_list_empty_or_full_of_none(lst_car)
    if is_empty_cars and is_empty_hint:
        raise Exception(
            "Parameters lstCar et lstHint cannot be empty at the same time")

    for line in codecs.open(f"assets/{lang}/{str(nb_car)}.txt", "r", "utf-8"):
        word = line.strip()
        searchByContent = is_search_by_content(word, list(lst_car), strict)
        searchByHint = is_search_by_hint(word, lst_hint)
        if searchByContent and is_empty_hint:
            yield word
        elif is_empty_cars and searchByHint:
            yield word
        elif searchByContent and searchByHint:
            yield word


def search_in_many_files(language, lst_car=[], lst_hint=[]):
    for i in reversed(range(1, len(lst_car)+1)):
        for m in search_in_file(language, nb_car=i, lst_car=lst_car, lst_hint=lst_hint):
            yield m