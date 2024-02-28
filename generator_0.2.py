import random
import string

class Generator:
    """ 
    Regular expressions start with a forward slash / followed by the pattern we want to match,
    and another forward slash / to end it.

    Capture groups and Lookarounds:
    (abc)       -   capture group
    (?:abc)     -   non-capturing group
    (?=abc)     -   positive lookahead
    (?!abc)     -   negative lookahead
    
    Quantifiers
    *           -   0 or more
    +           -   1 or more
    ?           -   0 or 1
    {x,y}       -   between x and y including
    {x}         -   exactly x times
    {x,}        -   x or more
    {,y}        -   up to and inluding y
    
    Bracket list
    [abc]       -   bracket list, any specified character in this list (here a, b, or c)
    [a-f]       -   any character in the range, here between a and f
    [^abc]      -   not any one character in this list 
    
    Logical operator
    a|b         -   a or b
    
    Metacharacters
    .           -   any character except new line
    \d          -   any one digit (same as [0-9])
    \D          -   any one non-digit (same as [^0-9])
    \w          -   any word character (same as [a-zA-Z0-9_])
    \W          -   any non word character (same as [^a-zA-Z0-9_])
    \s          -   any type of whitespace (whitespace characters are [ \n\r\t\f])
    \S          -   any type of non whitespace
    """

    def __init__(self, max_repeat) -> None:
        self.result = ""
        self.max_repeat = max_repeat


    def generate(self, regex_string):
        if regex_string[0] == '/' and regex_string[(len(regex_string)-1)] == '/':
            self.process_regex_string(regex_string[1:(len(regex_string)-2)])
        elif regex_string[0] != '/' and regex_string[(len(regex_string)-1)] != '/':
            self.process_regex_string(regex_string)
        else:
            print("wrong syntax")
        return self.result


    def process_regex_string(self, regex_string):
        """
        First check if there are capture groups between ( and )
        These needs to be processed including possible quantity part
        
        If there is no ( and ), its a regular regex string part
        """
        if '(' in regex_string:
            quantifier = {}
            # Find outer brackets pair
            outer_brackets = self.get_outer_brackets(regex_string)
            # Check if there is a quantifier behind the brackets
            if outer_brackets["Close"] < (len(regex_string) - 1):
                quantifier = self.check_for_quantifier(regex_string, outer_brackets["Close"]+1)
            else:
                # the closing bracket is the last character
                quantifier = {"Min" : 1, "Max" : 1, "Chars": 0}
            # There might be a piece of string before the first bracket which needs to be processed
            if outer_brackets["Open"] > 0:
                self.process_regex_string(regex_string[0:outer_brackets["Open"]])
            # TO BE IMPLEMENTED
            if regex_string[outer_brackets["Open"] + 1] == '?' and regex_string[outer_brackets["Open"] + 2] == ':':
                print("non capturing group")
            elif regex_string[outer_brackets["Open"] + 1] == '?' and regex_string[outer_brackets["Open"] + 2] == '=':
                print("positive lookahead")
            elif regex_string[outer_brackets["Open"] + 1] == '?' and regex_string[outer_brackets["Open"] + 2] == '!':
                print("negative lookahead")
            # /TO BE IMPLEMENTED    
            else:
                #print("capture group")
                # We process the capture group between the specified minimum and maximum by the quantifier
                random_amount = self.get_random_number_between(int(quantifier["Min"]), int(quantifier["Max"]))
                for i in range(random_amount):
                    self.process_regex_string(regex_string[outer_brackets["Open"]+1:outer_brackets["Close"]])
            # if there is more string after the closing bracket and possible quantifier, this needs to be processed as well
            if (len(regex_string)-1) > (outer_brackets["Close"] + quantifier["Chars"]):
                self.process_regex_string(regex_string[((outer_brackets["Close"] + quantifier["Chars"])+1):(len(regex_string))])
        else:
            # There are no brackets, so the whole string can be processed as a regular regex
            self.result += str(self.process_regular_regex(regex_string))


    def process_regular_regex(self, regex_string):
        """
        This string will process the regular string without groups
        """
        print("into process_regular_regex: {}".format(regex_string))
        temp_result = ""
        if '|' in regex_string:
            print("theres a logical operator")
            # TODO: the logical or should not be processed when inside brackets, it breaks
            regex_string = self.process_logical_or(regex_string)
        print("after the logical operator selection shizzle, the regex is: {}".format(regex_string))    
        index = 0
        while index < len(regex_string):
            quantifier = {}
            random_amount = None
            if regex_string[index] == '\\':
                print("escaped characters found")
                if (index + 2) < len(regex_string):
                    # there might be a quantifier
                    quantifier = self.check_for_quantifier(regex_string, index + 2)
                    random_amount = self.get_random_number_between(int(quantifier["Min"]), int(quantifier["Max"]))
                else:
                    # there will be no quantifier
                    quantifier["Chars"] = 0
                    random_amount = 1
                if regex_string[index+1] == 'd':
                    for i in range(random_amount):
                        temp_result += self.return_random_item_from_collection(string.digits)
                elif regex_string[index+1] == 'D':
                    for i in range(random_amount):
                        temp_result += self.return_random_item_from_collection(string.ascii_lowercase + string.ascii_uppercase + string.whitespace + string.punctuation)
                elif regex_string[index+1] == 'w':
                    for i in range(random_amount):
                        temp_result += self.return_random_item_from_collection(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_')
                elif regex_string[index+1] == 'W':
                    new_punctuation = self.remove_char_from_string(string.punctuation, '_')
                    for i in range(random_amount):
                        temp_result += self.return_random_item_from_collection(new_punctuation + string.whitespace)
                elif regex_string[index+1] == 's':
                    for i in range(random_amount):
                        temp_result += self.return_random_item_from_collection(string.whitespace)
                elif regex_string[index+1] == 'S':
                    for i in range(random_amount):
                        temp_result += self.return_random_item_from_collection(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation)
                elif regex_string[index+1] in [ '.','^','$','*','+','?','(',')','[', '{', '\\', '|']:
                    for i in range(random_amount):
                        temp_result += regex_string[index+1]
                # update the index according to the amount of characters that have been processed extra
                index = index + 1 + quantifier["Chars"]
            elif regex_string[index] == '[':
                print("square brackets found")
                closing_bracket = None
                for i in range((index + 1), len(regex_string)):
                    print("the i in the loop is: {}".format(i))
                    if regex_string[i] == ']':
                        closing_bracket = i
                        print("closing bracket in loop: {}".format(closing_bracket))
                        break
                bracket_collection = self.build_bracket_collection(regex_string[(index+1):closing_bracket])
                print("closing bracket: {}".format(closing_bracket))
                if (closing_bracket + 1) < len(regex_string):
                    # there might be a quantifier
                    print("theres still possibly a quantifier. closing bracket is at {} (searching for +1) and the length of the regex is {}".format(closing_bracket, len(regex_string)))
                    quantifier = self.check_for_quantifier(regex_string, closing_bracket + 1)
                    random_amount = self.get_random_number_between(int(quantifier["Min"]), int(quantifier["Max"]))
                else:
                    # there will be no quantifier
                    quantifier["Chars"] = 0
                    random_amount = 1
                for i in range(random_amount):
                    temp_result += self.return_random_item_from_collection(bracket_collection)
                difference = closing_bracket - index
                index = index + difference + quantifier["Chars"]
            elif regex_string[index] == '.':
                print("found a dot")
                if (index + 1) < len(regex_string):
                    quantifier = self.check_for_quantifier(regex_string, index + 1)
                    random_amount = self.get_random_number_between(int(quantifier["Min"]), int(quantifier["Max"]))
                else:
                    # there will be no quantifier
                    quantifier["Chars"] = 0
                    random_amount = 1
                whitespace = self.remove_char_from_string(string.whitespace, '\n')
                total = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation + whitespace
                for i in range(random_amount):
                    temp_result += self.return_random_item_from_collection(total)
                index = index + 1 + quantifier["Chars"]
            elif regex_string[index] in ['^', '$']:
                print("anchor tag detected")
                temp_result += ""
            else:
                if (index + 1) < len(regex_string):
                    # there might be a quantifier
                    quantifier = self.check_for_quantifier(regex_string, index + 1)
                    random_amount = self.get_random_number_between(int(quantifier["Min"]), int(quantifier["Max"]))
                else:
                    # there will be no quantifier
                    quantifier["Chars"] = 0
                    random_amount = 1
                for i in range(random_amount):
                    temp_result += regex_string[index]
                # update the index according to the amount of characters that have been processed extra
                index = index + quantifier["Chars"]
            index += 1
        print("returned from process_regular_regex: {}".format(temp_result))
        return temp_result


    def build_bracket_collection(self, regex_string):
        """
        Builds a collection based on whats between the brackets [ and ], either negative or positive
        """
        collection = []
        all_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.whitespace + string.punctuation
        ### Build up the negative collection
        if regex_string[0] == '^':
            index = 1
            temp = []
            while index < len(regex_string):
                if index < (len(regex_string)-2):
                    if (index +1) < len(regex_string) and regex_string[(index+1)] == '-':
                        for char in range(ord(regex_string[index]), ord(regex_string[(index+2)])+1):
                            temp.append(chr(char))
                        index += 2
                    elif regex_string[index] == '\\':
                        temp += self.process_escaped_character(regex_string[index+1])
                        # if regex_string[index+1] == 'd':
                        #     for char in string.digits:
                        #         temp.append(char)
                        # elif regex_string[index+1] == 'D':
                        #     for char in string.ascii_lowercase:
                        #         temp.append(char)
                        #     for char in string.ascii_uppercase:
                        #         temp.append(char)
                        #     for char in string.whitespace:
                        #         temp.append(char)
                        #     for char in string.punctuation:
                        #         temp.append(char)
                        # elif regex_string[index+1] == 'w':
                        #     for char in string.ascii_lowercase:
                        #         temp.append(char)
                        #     for char in string.ascii_uppercase:
                        #         temp.append(char)
                        #     for char in string.digits:
                        #         temp.append(char)
                        #     temp.append('_')
                        # elif regex_string[index+1] == 'W':
                        #     new_punctuation = self.remove_char_from_string(string.punctuation, '_')
                        #     for char in new_punctuation:
                        #         temp.append(char)
                        #     for char in string.whitespace:
                        #         temp.append(char)
                        # elif regex_string[index+1] == 's':
                        #     for char in string.whitespace:
                        #         temp.append(char)
                        # elif regex_string[index+1] == 'S':
                        #     for char in string.ascii_lowercase:
                        #         temp.append(char)
                        #     for char in string.ascii_uppercase:
                        #         temp.append(char)
                        #     for char in string.digits:
                        #         temp.append(char)
                        #     for char in string.punctuation:
                        #         temp.append(char)
                        # elif regex_string[index+1] in [ '.','^','$','*','+','?','(',')','[', '{', '\\', '|']:
                        #     temp.append(char(regex_string[index+1]))
                        index += 1
                    else:
                        temp.append(regex_string[index])
                elif index < (len(regex_string)-1):
                    if regex_string[index] == '\\':
                        temp += self.process_escaped_character(regex_string[index+1])
                        # if regex_string[index+1] == 'd':
                        #     for char in string.digits:
                        #         temp.append(char)
                        # elif regex_string[index+1] == 'D':
                        #     for char in string.ascii_lowercase:
                        #         temp.append(char)
                        #     for char in string.ascii_uppercase:
                        #         temp.append(char)
                        #     for char in string.whitespace:
                        #         temp.append(char)
                        #     for char in string.punctuation:
                        #         temp.append(char)
                        # elif regex_string[index+1] == 'w':
                        #     for char in string.ascii_lowercase:
                        #         temp.append(char)
                        #     for char in string.ascii_uppercase:
                        #         temp.append(char)
                        #     for char in string.digits:
                        #         temp.append(char)
                        #     temp.append('_')
                        # elif regex_string[index+1] == 'W':
                        #     new_punctuation = self.remove_char_from_string(string.punctuation, '_')
                        #     for char in new_punctuation:
                        #         temp.append(char)
                        #     for char in string.whitespace:
                        #         temp.append(char)
                        # elif regex_string[index+1] == 's':
                        #     for char in string.whitespace:
                        #         temp.append(char)
                        # elif regex_string[index+1] == 'S':
                        #     for char in string.ascii_lowercase:
                        #         temp.append(char)
                        #     for char in string.ascii_uppercase:
                        #         temp.append(char)
                        #     for char in string.digits:
                        #         temp.append(char)
                        #     for char in string.punctuation:
                        #         temp.append(char)
                        # elif regex_string[index+1] in [ '.','^','$','*','+','?','(',')','[', '{', '\\', '|']:
                        #     temp.append(char(regex_string[index+1]))
                        index += 1
                    else:
                        temp.append(regex_string[index])
                else:
                    temp.append(regex_string[index])
                index += 1
            for char in all_chars:
                if char not in temp:
                    collection.append(char)
        ### Build up the positive collection
        else:
            index = 0
            while index < len(regex_string):
                if index < (len(regex_string)-2):
                    if (index +1) < len(regex_string) and regex_string[(index+1)] == '-':
                        for char in range(ord(regex_string[index]), ord(regex_string[(index+2)])+1):
                            collection.append(chr(char))
                        index += 2
                    elif regex_string[index] == '\\':
                        collection += self.process_escaped_character(regex_string[index+1])
                        # if regex_string[index+1] == 'd':
                        #     for char in string.digits:
                        #         collection.append(char)
                        # elif regex_string[index+1] == 'D':
                        #     for char in string.ascii_lowercase:
                        #         collection.append(char)
                        #     for char in string.ascii_uppercase:
                        #         collection.append(char)
                        #     for char in string.whitespace:
                        #         collection.append(char)
                        #     for char in string.punctuation:
                        #         collection.append(char)
                        # elif regex_string[index+1] == 'w':
                        #     for char in string.ascii_lowercase:
                        #         collection.append(char)
                        #     for char in string.ascii_uppercase:
                        #         collection.append(char)
                        #     for char in string.digits:
                        #         collection.append(char)
                        #     collection.append('_')
                        # elif regex_string[index+1] == 'W':
                        #     new_punctuation = self.remove_char_from_string(string.punctuation, '_')
                        #     for char in new_punctuation:
                        #         collection.append(char)
                        #     for char in string.whitespace:
                        #         collection.append(char)
                        # elif regex_string[index+1] == 's':
                        #     for char in string.whitespace:
                        #         collection.append(char)
                        # elif regex_string[index+1] == 'S':
                        #     for char in string.ascii_lowercase:
                        #         collection.append(char)
                        #     for char in string.ascii_uppercase:
                        #         collection.append(char)
                        #     for char in string.digits:
                        #         collection.append(char)
                        #     for char in string.punctuation:
                        #         collection.append(char)
                        # elif regex_string[index+1] in [ '.','^','$','*','+','?','(',')','[', '{', '\\', '|']:
                        #     collection.append(char(regex_string[index+1]))
                        index += 1
                    else:
                        collection.append(regex_string[index])
                elif index < (len(regex_string)-1):
                    if regex_string[index] == '\\':
                        collection += self.process_escaped_character(regex_string[index+1])
                        # if regex_string[index+1] == 'd':
                        #     for char in string.digits:
                        #         collection.append(char)
                        # elif regex_string[index+1] == 'D':
                        #     for char in string.ascii_lowercase:
                        #         collection.append(char)
                        #     for char in string.ascii_uppercase:
                        #         collection.append(char)
                        #     for char in string.whitespace:
                        #         collection.append(char)
                        #     for char in string.punctuation:
                        #         collection.append(char)
                        # elif regex_string[index+1] == 'w':
                        #     for char in string.ascii_lowercase:
                        #         collection.append(char)
                        #     for char in string.ascii_uppercase:
                        #         collection.append(char)
                        #     for char in string.digits:
                        #         collection.append(char)
                        #     collection.append('_')
                        # elif regex_string[index+1] == 'W':
                        #     new_punctuation = self.remove_char_from_string(string.punctuation, '_')
                        #     for char in new_punctuation:
                        #         collection.append(char)
                        #     for char in string.whitespace:
                        #         collection.append(char)
                        # elif regex_string[index+1] == 's':
                        #     for char in string.whitespace:
                        #         collection.append(char)
                        # elif regex_string[index+1] == 'S':
                        #     for char in string.ascii_lowercase:
                        #         collection.append(char)
                        #     for char in string.ascii_uppercase:
                        #         collection.append(char)
                        #     for char in string.digits:
                        #         collection.append(char)
                        #     for char in string.punctuation:
                        #         collection.append(char)
                        # elif regex_string[index+1] in [ '.','^','$','*','+','?','(',')','[', '{', '\\', '|']:
                        #     collection.append(char(regex_string[index+1]))
                        index += 1
                    else:
                        collection.append(regex_string[index])
                else:
                    collection.append(regex_string[index])
                index += 1
        return collection


    def process_escaped_character(self, character):
        """
        Builds and returns a list of characters based on the escaped character
        """
        temp = []
        if character == 'd':
            for char in string.digits:
                temp.append(char)
        elif character == 'D':
            for char in string.ascii_lowercase:
                temp.append(char)
            for char in string.ascii_uppercase:
                temp.append(char)
            for char in string.whitespace:
                temp.append(char)
            for char in string.punctuation:
                temp.append(char)
        elif character == 'w':
            for char in string.ascii_lowercase:
                temp.append(char)
            for char in string.ascii_uppercase:
                temp.append(char)
            for char in string.digits:
                temp.append(char)
            temp.append('_')
        elif character == 'W':
            new_punctuation = self.remove_char_from_string(string.punctuation, '_')
            for char in new_punctuation:
                temp.append(char)
            for char in string.whitespace:
                temp.append(char)
        elif character == 's':
            for char in string.whitespace:
                temp.append(char)
        elif character == 'S':
            for char in string.ascii_lowercase:
                temp.append(char)
            for char in string.ascii_uppercase:
                temp.append(char)
            for char in string.digits:
                temp.append(char)
            for char in string.punctuation:
                temp.append(char)
        elif character in [ '.','^','$','*','+','?','(',')','[', '{', '\\', '|']:
            temp.append(character)
        return temp


    def process_logical_or(self, regex_string):
        """
        This will check on logical or operators, and return one of the possible
        substrings randomly
        """
        or_operator_indeces = []
        for index in range(len(regex_string)):
            if regex_string[index] == '|':
                or_operator_indeces.append(index)
        amount_operators = len(or_operator_indeces)
        random_part = self.get_random_number_between(0, amount_operators)
        if random_part == 0:
            return regex_string[0:or_operator_indeces[random_part]]
        elif random_part == amount_operators:
            return regex_string[(or_operator_indeces[(random_part-1)]+1):(len(regex_string))]
        else:
            return regex_string[((or_operator_indeces[(random_part - 1)])+1):or_operator_indeces[random_part]]


    def get_outer_brackets(self,regex_string) -> dict:
        """
        Finds the first opening bracket in a string and its corresponding closing bracket
        Needs to keep track of brackets in between to find the right closing bracket
        """
        # find opening bracket
        opening_bracket_index = None
        closing_bracket_index = None
        for index, char in enumerate(regex_string):
            if char == '(':
                opening_bracket_index = index
                break
        # find the corresponding closing bracket
        extra_opening_brackets = 0
        for index in range(opening_bracket_index + 1, len(regex_string)):
            if regex_string[index] == ')' and extra_opening_brackets == 0:
                closing_bracket_index = index
                break
            elif regex_string[index] == '(':
                extra_opening_brackets += 1
            elif regex_string[index] == ')' and extra_opening_brackets > 0:
                extra_opening_brackets -= 1
        brackets = {"Open" : opening_bracket_index, "Close" : closing_bracket_index}
        return brackets


    def check_for_quantifier(self, regex_string, start_index):
        """
        Returns the minimum and maximum of found quantifier as well as
        how many characters were found for the quantifier
        """
        if regex_string[start_index] == '*':
            return {"Min" : 0, "Max" : None, "Chars": 1}
        elif regex_string[start_index] == '+':
            return {"Min" : 1, "Max" : None, "Chars": 1}
        elif regex_string[start_index] == '?':
            return {"Min" : 0, "Max" : 1, "Chars": 1}
        elif regex_string[start_index] == '{':
            for index in range(start_index, len(regex_string)):
                if regex_string[index] == '}':
                    char_amount = (index + 1) - start_index
                    values = self.process_quantifier_block(regex_string[start_index:index+1])
                    values["Chars"] = char_amount
                    return values
        else:
            return {"Min" : 1, "Max" : 1, "Chars": 0}


    def process_quantifier_block(self, block):
        """
        If there is a comma in the block, it means there is a separate minimum and maximum value.
        If there is no comma, it must be exactly the specified number -> min and max are the same.
        """
        min_value = None
        max_value = None
        length = len(block)
        if ',' in block:
            comma_index = block.index(',')
            if (comma_index - 1) != 0:
                min_value = block[1:comma_index]
            if (comma_index + 1) != (length - 1):
                max_value = block[(comma_index + 1):(length - 1)]
        else:
            min_value = block[1:(length - 1)]
            max_value = block[1:(length - 1)]
        values = {"Min" : min_value, "Max" : max_value}
        return values


    def get_random_number_between(self, min_value, max_value):
        """
        Returns a random number between and including min_value and max_value
        If min_value is None, it is set to 0
        If max_value is None, it is set to self.MAX_REPEAT
        """
        if not min_value:
            min_value = 0
        if not max_value:
            max_value = self.max_repeat
        return random.randint(min_value, max_value)


    def return_random_item_from_collection(self, collection):
        """
        Returns a random item from the provided collection
        """
        return random.choice(collection)


    def remote_item_from_collection(self, collection, item):
        """
        If item is in collection, returns the collection minus the item,
        else returns unaltered collection
        """
        if item in collection:
            collection.remove(item)
            return collection
        else:
            return collection


    def remove_char_from_string(self, regex_string, char):
        """
        If character is in the string, returns the string minus the characters,
        else returns the unaltered string
        """
        if char in regex_string:
            return regex_string.replace(char, "")
        else:
            return regex_string


test = Generator(100)
print("From what regex would you like the string to be generated?")
input = input()
result = test.generate(input)
print("The result is: {}".format(result))