import time,string

dic_word = {} #for mapping word to its frequency in source file

def add_from_big() :    
    """This function is to extract every word in big.txt
    to data structure (dic_word)"""

    start = time.time()

    print("Loading...")
    print("Setup data structure from big.txt...")

    global dic_word
    
    dic_word.clear() #clear dictionary in case user call this function again
                      #to reset
    list_word = []
    
    with open("big.txt") as myFile :
            #make into string->easy for spliting into list
            content = myFile.read() 

            #eliminate non alphabets by replacing them with whitespace
            #except "'" character to include word with "'" such as don't, etc.
            nonalpha = string.punctuation + string.whitespace + string.digits
            nonalpha = nonalpha.replace( "'", '' )
            for char in nonalpha :
                content = content.replace( char, ' ' )

            content = content.lower()
            list_word = content.split()#still have 2 or more same words
            
            #make dictionary by mapping each word to its frequency
            for key in list_word :
                if key in dic_word :
                    dic_word[ key ] = dic_word[ key ] + 1
                else:
                    dic_word[ key ] = 1
        
    
    print( "Setup complete" )        
    print( "Processing time:  {:.2f} sec".format( time.time() - start ) )
    print()
    
def add_from_word_list() :
    """This function is to extract every word in word_list.txt
    to data structure (dic_word)"""
    start = time.time()

    global dic_word

    print("Loading...")
    print("Adding data from word_list.txt...")

    list_word = []
    with open("word_list.txt") as myFile :
        #make into string->easy for spliting into list
        content = myFile.read() 

        #eliminate non alphabets by replacing them with whitespace
        #except "'" character to include word with "'" such as don't, etc.
        nonalpha = string.punctuation + string.whitespace + string.digits
        nonalpha = nonalpha.replace( "'", '' )
        for char in nonalpha :
            content = content.replace( char, ' ' )

        content = content.lower()

        list_word = content.split()#still have 2 or more same words

        #make dictionary by mapping each word to its frequency
        for key in list_word :
                if key in dic_word :
                    dic_word[ key ] = dic_word[ key ] + 1
                else:
                    dic_word[ key ] = 1
        
    print( "Setup complete" )        
    print( "Processing time:  {:.2f} sec".format( time.time() - start ) )
    print()

add_from_big()
print( "Guide to use autocorrect function :" )
print( '1. Type "autocorrect(input_word)" where "input_word" is word that need to be corrected' )
print( '2. Press enter to invoke autocorrect function' )
print()
print( 'Guide to add a word into data structure:' )
print( '1. Type "add(input_word)" where "input_word" is word that want to be added' )
print( '2. Press enter to invoke add function' )
print()
print( 'Guide to add both big.txt and word_list.txt into data structure:' )
print( '1. Type "add_from_word_list()"' )
print( '2. Press enter to invoke the function' )
print()
print( 'Guide to reset data structure and load only big.txt:' )
print( '1. Type "add_from_big()"' )
print( '2. Press enter to invoke the function' )
print()

def add_word( word ) :
    """This function is to add a word to dictionary"""
   
    global dic_word
    start  = time.time()
    
    dic_word[ word ] = 1

    print( "The word is added" )
    print( "Processing time:  {:.2f} sec".format( time.time() - start ) )

def worddistance ( word1, word2 ):
    """This function is to compute distance between 2 words."""
    #The principle of this function is to detect subtituion, insertion,
    #deletion, and transposition needed to transform word1 to word2
    #The idea is based on Damerau–Levenshtein_distance
    #Credit to  Frederick J. Damerau and Vladimir I. Levenshtein
    #Source http://en.wikipedia.org/wiki/Damerau–Levenshtein_distance
    len1 = len( word1 )
    len2 = len( word2 )

    #determin which word is longer
    if (len1 > len2):
        maxlen, minlen = len1, len2
        maxword, minword = word1, word2
    else:
        maxlen, minlen = len2, len1
        maxword, minword = word2, word1

    i = 0
    j = 0
    distance = 0
    ins_or_del = abs( len1 - len2 ) #insertion or deletion needed


    if ( maxword.find( minword ) != -1 ) : #when minword is substring of maxword
        return ins_or_del                   #distance should be length difference

    #compute distance
    while i < minlen and j < maxlen :
        if (minword[i] == maxword[j]) :
                i += 1
                j += 1
        
        #detect if insertion or deletion needed
        elif ( ins_or_del and j < maxlen - 1 and minword[i] == maxword[j+1] ):
            distance += 1
            j += 1
            ins_or_del -= 1

        #detect if transposition needed such as 'ab' to 'ba'
        elif ( i < minlen - 1 and j < maxlen -1 and minword[i] == maxword[j+1] \
                and minword[i+1] ==  maxword[j] ) :                                         
            distance += 1
            i += 2
            j += 2

        #need substitution
        else:
            distance += 1
            i += 1
            j += 1
    
    return distance + ins_or_del

def autocorrect( target ) :
    """This function is invoked to correct the input word"""
    start = time.time()

    target = target.lower()

    #check invalid input
    if (target == '' or target.find(" ") != -1 ):
        print( "Your input is invalid" )
        print( "Please call the function again" )
        return

    if target in dic_word : #no need to compute distance if target is correct
        print("The spelling is correct")
        print( "Processing time:  {:.2f} sec".format( time.time() - start ) )
        return

    freq_word = {}
    limit = 10000000
    len_target = len( target )

    #search correct words with minimal distance
    for word in dic_word :
        #avoid unfiltered word such as th' , 'god, etc
        if word[0] == "'" or word[-1:-2:-1] == "'" :
            continue

        #assume length difference less than 2
        if abs( len( word ) - len_target ) > 2 :
            continue                            

        distance1 = worddistance( target, word )

        if ( distance1 > limit ) : #no need include distance greater than limit
            continue               

        #update limit and reset dictionary to ensure minimal distance
        if ( distance1 < limit ) : 
            limit = distance1     
            freq_word = {}

        freq_word[ word ] = dic_word[ word ]       

    if not freq_word : 
        print("Sorry, there are no solution.")
        print( "Processing time:  {:.2f} sec".format( time.time() - start ) )
        return
           
    len_cor = len( freq_word )
    if (len_cor > 10 ): #limit result when result > 10 by choosing same first letter
        list_result = [word for word in freq_word if word[0] == target[0]]

        if not list_result : #use previous result if no new result
            list_result = list( freq_word.keys() )

        len_cor = len( list_result )
    else:
        list_result = list( freq_word.keys() )

    #print all results
    print( "Did you mean: ", end = "" )
    result = list_result[0]
    if len_cor > 1 :
        result = ", ".join( list_result[0: len_cor-1] )
        result = result + ", or " + list_result[len_cor - 1] + "?"
    print( result )
    print( "Processing time:  {:.2f} sec".format( time.time() - start ) )

    #check if user need most likely word
    #the most likely word is the one with the highest frequency
    if ( len_cor > 1) :
        need_most_likely = input( "Do you want the most likely word?(y/n)" )
        if need_most_likely.lower() == 'y':
            start = time.time()
            print( "The most likely word is:", max( list_result, key = freq_word.get ) )
            print( "Processing time:  {:.2f} sec".format( time.time() - start ) )
        else:
            print("Thank you")
    

