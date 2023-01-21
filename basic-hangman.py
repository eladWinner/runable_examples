# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name: object) -> object:
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def main():

    def choose_word(file_path, index):
        """

        :param file_path: self explanatory
        :param index: word spot in file ( with looping )
        :return:  the selected word
        """
        # dictionary={} # not used now
        words = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines :
                line=line.strip('\n')
                for word in line.split(" "):
                    #dictionary[word]=False
                    words.append(word)
        # number_of_unique_words = len(dictionary)
        index = (int(index) -1)%len(words) # instead of repeating
        return words[index]

    def check_valid_input(letter_guessed, old_letters_guessed):
        """

        :param letter_guessed: the guess
        :param old_letters_guessed: history of old guesses
        :return: boolean if valid
        """
        if len(letter_guessed)!=1 or not isinstance(letter_guessed, str):
            return False
        char_value = ord(letter_guessed)
        if char_value >= ord('a'): # A= 65 , a=97
            char_value -= ord('a')
        else:
            char_value -= ord('A')
        if char_value >=(ord('z')-ord('a')+1) or char_value <0 :
            return False
        return not old_letters_guessed[char_value] # returns the opposite of history if played did guess latter
        #tl:dr ' if player did **NOT** guess that letter before.'

    def try_update_letter_guessed(letter_guessed, old_letters_guessed):
        """

        :param letter_guessed: above
        :param old_letters_guessed:
        :return: boolean if manged to replace letter
        """
        if check_valid_input (letter_guessed, old_letters_guessed):
            old_letters_guessed[ord(letter_guessed.lower())-ord('a')] = True
            return True
        # no need for else
        print("X")
        first = True
        # prints in order letters guessed before
        for i in range(ord('z')-ord('a')+1):
            if (old_letters_guessed[i]):
                if not first:
                    print(' -> ',end='')
                first= False
                print(chr(i+ord('a')),end='')
        if not first:
            print()
        return False

    def show_hidden_word(secret_word, old_letters_guessed):
        """

        :param secret_word: self
        :param old_letters_guessed: above
        :return: string of visible parts of secret word based on history
        """
        string_builder =[]
        aCHAR = ord('a')
        first = True
        for i in secret_word:
            if not first:
                string_builder.append(" ")
            first = False
            if old_letters_guessed[ord(i)-aCHAR]:
                string_builder.append(i)
            else:
                string_builder.append("_")
        return ''.join(string_builder)

    def check_win(secret_word, old_letters_guessed):
        """

        :param secret_word:
        :param old_letters_guessed:
        :return: boolean if won
        """
        for i in secret_word:
            if not old_letters_guessed[ord(i)-ord('a')]:
                return False # leave function
        return True
    # aiding functions
    #############################################
    # start function

    def Start_Game():
        """
        :return: void . starts game
        """
        MAX_TRIES = 6
        old_letters_guessed = [False for i in range(ord('z')-ord('a')+1)] # The English Alphabet (or Modern English Alphabet) today consists of 26 letters
        secret_word = ""
        num_of_tries = 0
        HANGMAN_ASCII_ART = """
      _    _                                         
     | |  | |                                        
     | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
     |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
     | |  | | (_| | | | | (_| | | | | | | (_| | | | |
     |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                          __/ |                      
                         |___/"""
        HANGMAN_PHOTOS = [
            """
        x-------x
            """
            ,"""
        x-------x
        |
        |
        |
        |
        |
            """
            ,"""
        x-------x
        |       |
        |       0
        |
        |
        |
            """
            ,"""
        x-------x
        |       |
        |       0
        |       |
        |
        |
            """
            ,"""
        x-------x
        |       |
        |       0
        |      /|\\
        |
        |
            """
            ,"""
        x-------x
        |       |
        |       0
        |      /|\\
        |      /
        |
    
            """
            ,"""
        x-------x
        |       |
        |       0
        |      /|\\
        |      / \\
        |
            """
        ]
        # Print the Welcome Screen
        print(HANGMAN_ASCII_ART)
        print(MAX_TRIES)
        print()

        # ask for file paths and index
        file_path = input("Enter file path: ")
        index = input("Enter index: ")
        secret_word = choose_word(file_path, index)
        secret_word = secret_word.lower()

        # start game loop
        print("Let’s start!\n")
        print(HANGMAN_PHOTOS[num_of_tries])
        print(show_hidden_word(secret_word, old_letters_guessed))
        print()

        # game has two exit conditions using too many tries or winning
        while num_of_tries < MAX_TRIES:
            guess = input("Guess a letter: ")
            if try_update_letter_guessed(guess, old_letters_guessed):
                if secret_word.count(guess)>0:
                    if check_win(secret_word ,old_letters_guessed):
                        print(show_hidden_word(secret_word, old_letters_guessed))
                        print("WIN")
                        # exit condition 2
                        return
                else:
                    print(":(")
                    num_of_tries = num_of_tries + 1
                    print(HANGMAN_PHOTOS[num_of_tries])
                print(show_hidden_word(secret_word, old_letters_guessed))
        # exit condition 1
        print("LOSE")
        return
    # functions
    #########################
    # code
    Start_Game()


if __name__ == '__main__':
    main()


