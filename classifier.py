import re
from math import log


# счётчик писем
lettersCnt = 0
# счётчик для спамовых писем
spamCnt = 0
# словарь формата {слово : [кол-во встреч в спам-письмах, кол-во встреч не в спам письмах]}
cntDict = dict()


def isSpamWord(spam_number: int, letters_number: int = lettersCnt) -> float:
    '''
    numOfLet = по дефолту всем письмам
    Возвращает вероятноть того, что слово является спамовым.
    '''
    # используется сглаживание Лапласа
    return (spam_number+1)/(letters_number+2)


def isSpamLetter(words: set[str]) -> bool:
    '''
    Возвращает True, если вероятность того, что письмо спам > вероятности, что не спам.
    False, в обратном случае.
    '''
    spam_robability = log(spamCnt/lettersCnt)
    ham_probability = log((lettersCnt-spamCnt)/lettersCnt)
    for word in words:
        word_counts = cntDict.get(word)
        if word_counts is None:
            word_counts = [1, 1]
        spam_robability += log(isSpamWord(word_counts[0], spamCnt))
        ham_probability += log(isSpamWord(word_counts[1], spamCnt))

    return spam_robability > ham_probability


def readLetters(input: str) -> list[str]:
    '''
    Считывает и возвращает список писем. Увеличивает счётчик количества писем.
    '''
    global lettersCnt
    with open(input, 'r', encoding='utf-8') as fin:
        data = fin.read()
    letters = data.split('\n')
    lettersCnt += len(letters)
    return letters


def train(input: str):
    """
    "Обучает", используя полученные тренировочные данные.
    """
    global spamCnt
    letters = readLetters(input)  # получаем список писем
    for letter in letters:
        split_data = letter.split('\t', 1)
        if split_data[0] == "spam":
            spamCnt += 1

        # разбиваем текст письма на слова
        words = set(re.sub(r'[.,"\'-?:!;]', '', split_data[1].lower()).split())
        # заполняем словарь количеством спама и не спама
        for word in words:
            word_counts = cntDict.get(word)
            if word_counts is None:
                word_counts = [0, 0]
            if split_data[0] == "spam":
                word_counts[0] += 1
            else:
                word_counts[1] += 1
            cntDict.update({word: word_counts})


def test(input: str):
    """
    Высчитывает процент правильно классифицированных писем,
    используя тестовые данные, отличающиеся от тренировочных.
    """
    truePredictonCnt = 0
    letters = readLetters(input)  # получаем список писем
    for letter in letters:
        split_data = letter.split('\t', 1)
        # разбиваем текст письма на слова
        words = set(re.sub(r'[.,"\'-?:!;]', '', split_data[1].lower()).split())
        if (split_data[0] == "spam") == (isSpamLetter(words)):
            truePredictonCnt += 1
    # вычисляем долю верно определенных среди всех писем
    print(f"Accuracy: {truePredictonCnt/len(letters):.3%}")


if __name__ == "__main__":
    train("data\\train_data.txt")
    test("data\\test_data.txt")
