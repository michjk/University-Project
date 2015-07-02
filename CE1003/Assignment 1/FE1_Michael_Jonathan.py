import time

f = open("big.txt").read()
#       A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
      
def listing2 (myFile1,myFile2):
    start = time.time()
    list_line = myFile1.split('\n')
    list_line2 = myFile2.split('\n')
    print("Split text into list takes {}".format(time.time()-start))
    list_line.extend(list_line2)
    list_words = []
    for line in list_line:
        word = ''
        #print(line)
        for char in line:
            if char.isalpha():
                word = word + char.lower()
            elif word!='':
                list_words.append(word)
                #print(list_words)
                word = ''
                #a = input()
        if (word!='') :
            list_words.append(word)
    net = time.time()-start
    print("Listing time {:0.3f} sec".format(net))
    return list_words

def count_words (list_words) :
    dict_words = {}
    start = time.time()
    for key in list_words :
        if key in dict_words :
            dict_words[key]=dict_words[key]+1
        else :
            dict_words[key] = 1
    net = time.time()-start
    print("counting time {:0.3f} sec".format(net))
    return dict_words

list_words = count_words(listing2(open('big.txt').read(),open('word_list.txt').read()))

#alphabet = 'abcdefghijklmnopqrstuvwxyz'

def worddistance (word1,word2):
    len1 = len(word1)
    len2 = len(word2)
    dp = [[0 for i in range(len2+1)] for j in range(len1+1)]
    for i in range (0,len1+1):
        dp[i][0] = i
    for j in range (0,len2+1):
        dp[0][j] = j
    for j in range(1,len2+1):
        for i in range(1,len1+1):
            if word1[i-1]==word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1,dp[i-1][j-1]+1)
    return dp[len1][len2]

def autocorrect (word) :
    start = time.time()
    chk = True
    list_cor = []
    list_f = []
    for target in list_words :
        if (abs(len(target)-len(word))>1):
            continue
        val = worddistance(word,target)
        if val <= 1:
            if val==0:
                print("The spelling is correct")
                chk = False
                break
            else:
                list_cor.append(target)
                list_f.append(list_words[target])
    lencor = len(list_cor)
    if not lencor : lencor +=1
    sum1 = sum(list_f)
    avg = sum1//lencor
    if chk:
        print("Did you mean: ",end="")
        for j in range(0,lencor) :
            if j==lencor-1:
                if (list_f[j]>=2) : print("or",list_cor[j]+"?")
            else:
                if (list_f[j]>=2) : print(list_cor[j]+", ",end='')
    net = time.time()-start
    print("counting time {:0.3f} sec".format(net))
    
while (1):
    word = input("please input a word :")
    autocorrect(word)











