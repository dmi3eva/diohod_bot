def deEmojify(inputString):
    returnString = inputString
    emoticons = ['\U0001F4F8', '\U0001F4F0', '\U0001F3AF', '\U0001F43E', '\U0001F3E0', '\U0001F32A', '\U0001F4F7',
                 '\U0001F409', '\U0001F3E0', '\U0001F6F8',
                 'Программу пишите прямо в сообщении']
    for _emoticon in emoticons:
        returnString = returnString.replace(_emoticon+' ', '')

    while '\n\n' in returnString:
        returnString = returnString.replace('\n\n', '\n')

    while ' \n' in returnString:
        returnString = returnString.replace(' \n', '\n')
    return returnString