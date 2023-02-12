# This is a sample Python script.

MAX_tries =6
class hang_man():
    def __init__(self):
        self.MAX_TRIES = MAX_tries
        self.guessed_letters_histogram = [False for i in range(ord('z')-ord('a')+1)] # The English Alphabet (or Modern English Alphabet) today consists of 26 letters
        self.secret_word = ""
        self.current_guess_num = 0
        self.HANGMAN_ASCII_ART,self.HANGMAN_PHOTOS = self.load_art()

    def load_art(self):
        return  """
      _    _                                         
     | |  | |                                        
     | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
     |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
     | |  | | (_| | | | | (_| | | | | | | (_| | | | |
     |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                          __/ |                      
                         |___/""",[
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
    def Start_Game(self):
        """
        :return: void . starts game
        """
        def print_startscreen():
            print(self.HANGMAN_ASCII_ART)
            print(self.MAX_TRIES)
            print()

        def start_inputs(): # ask for file paths and index
            def choose_word(file_path, index): # is reading twice faster than , 1 read+ 1 write copy?
                words = []
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines :
                        line=line.strip('\n')
                        for word in line.split(" "):
                            words.append(word)
                index = (int(index) -1)%len(words) # instead of repeating
                return words[index]
            file_path = input("Enter file path: ")
            index = input("Enter index: ")
            self.secret_word = choose_word(file_path, index).lower()

        def print_start_squance():
            print("Let’s start!\n")
            print(self.HANGMAN_PHOTOS[self.current_guess_num])
            print(show_hidden_word(self.secret_word, self.guessed_letters_histogram))
            print()

        def valid_guess():
            def check_valid_input(letter_guessed, guessed_letters_histogram):
                if not isinstance(letter_guessed, str) or len(letter_guessed)!=1:
                    return False
                if not letter_guessed.isalpha():
                    return False
                char_value = ord(letter_guessed.lower())-ord('a')
                return not guessed_letters_histogram[char_value] # returns the letter is not in guess history

            def try_update_letter_guessed(letter_guessed, guessed_letters_histogram):
                def prtint_previous_guess(guess_hist): # history and histogram
                    for i in range(ord('z')-ord('a')+1):
                        if (guess_hist[i]):
                            if not first:
                                print(' -> ',end='')
                            first= False
                            print(chr(i+ord('a')),end='')

                if check_valid_input (letter_guessed, guessed_letters_histogram):
                    guessed_letters_histogram[ord(letter_guessed.lower())-ord('a')] = True
                    return True
                print("X") # means in correct guess
                first = True
                prtint_previous_guess(guessed_letters_histogram)# prints in order letters guessed before
                if not first:
                    print()
                return False

            guess = input("Guess a letter: ")
            if try_update_letter_guessed(guess, self.guessed_letters_histogram):
                return guess
            return valid_guess() # while true

        def check_win_condation():
            if self.check_win(self.secret_word ,self.guessed_letters_histogram):
                print(self.show_hidden_word(self.secret_word, self.guessed_letters_histogram))
                print("WIN")
                return True
            return False

        def show_hidden_word(secret_word, guessed_letters_histogram):
            string_builder =[]
            first = True
            for i in secret_word:
                if not first:
                    string_builder.append(" ")
                first = False
                if guessed_letters_histogram[ord(i)-ord('a')]:
                    string_builder.append(i)
                else:
                    string_builder.append("_")
            return ''.join(string_builder)

        print_startscreen()
        start_inputs()
        print_start_squance()
        # start game loop
        while self.current_guess_num < self.MAX_TRIES:# game has two exit conditions using too many tries or winning
            guess=valid_guess()
            if self.secret_word.count(guess)>0:
                if check_win_condation():
                    return #exit game
            else:
                print(":(")
                self.current_guess_num = self.current_guess_num + 1
                print(self.HANGMAN_PHOTOS[self.current_guess_num])
            print(show_hidden_word(self.secret_word, self.guessed_letters_histogram))
        # exit game lose condition
        print("LOSE")
        return


        
def main():
    hang_man_game=hang_man()
    hang_man_game.Start_Game()

if __name__ == '__main__':
    main()
