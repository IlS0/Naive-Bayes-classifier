import re
import math

spamCnt = 0
lettersCnt = 0
wordDict = dict() #словарь формата {слово : [кол-во встреч в спам-письмах, кол-во встреч не в спам письмах]}

def isSpamWord(numOfSpam,numOfLet=lettersCnt):
    '''
    numOfLet = по дефолту всем письмам
    Возвращает вероятноть того, что слово является спамовым + используется сглаживание Лапласа.
    '''
    return (numOfSpam+1)/(numOfLet+2)


def isSpamLetter(letter):
    '''
    Возвращает одно из значений: true, false.
    True, если вероятность того, что оно спам > вероятности, что не спам.
    False, в обратном случае.
    '''
    spamProb = math.log(spamCnt/lettersCnt)
    hamProb = math.log((lettersCnt-spamCnt)/lettersCnt)
    for word in letter:
        nums = wordDict.get(word)
        if nums is None:
            nums = [1, 1]
        spamProb += math.log(isSpamWord(nums[0], spamCnt))
        hamProb += math.log(isSpamWord(nums[1], spamCnt))

    return spamProb>hamProb


def readLetters(inp):
    '''
    Считывает и возвращает список писем. Увеличивает счётчик количества писем.
    '''
    global lettersCnt
    with open(inp, 'r', encoding='utf-8') as fin:
        data = fin.read()
    letters = data.split('\n')
    lettersCnt += len(letters)
    return letters


def learn(inp):
    """
    "обучает", используя полученные данные.
    """
    global spamCnt
    letters = readLetters(inp)#получаем список писем
    lenLets = len(letters)
    for i in range(lenLets):
        tmp = letters[i].split('\t', 1)
        if tmp[0] == "spam":
            spamCnt += 1
        words = set(re.sub(r'[.,"\'-?:!;]', '', tmp[1].lower()).split())#разбиваем письмо на слова
        for word in words:
            nums = wordDict.get(word)
            if nums is None:
                nums = [0, 0]
            if tmp[0] == "spam":
                nums[0] += 1
            else:
                nums[1] += 1
            wordDict.update({word: nums})


def work(inp):
    """
    высчитывает процент правильно классифицированных писем.
    """
    trueCnt =0 
    letters = readLetters(inp)#получаем список писем
    lenLets = len(letters)
    for i in range(lenLets):
        tmp = letters[i].split('\t', 1) 
        words = set(re.sub(r'[.,"\'-?:!;]', '', tmp[1].lower()).split())#разбиваем письмо на слова
        if (tmp[0]=="spam") == (isSpamLetter(words)):
            trueCnt+=1
    print(f"Accuracy: {trueCnt/lenLets*100}%")


if __name__ == "__main__":
    learn("learnInp.txt")
    work("chekInp.txt")
