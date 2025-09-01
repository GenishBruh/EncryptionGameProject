# ZigZag Encryption (or rail fence)

def zigzag_cipher(text, key):

    # Take out spaces
    stripped_text = "".join(text.split())

    # Create a 2d list with placeholders in it

    rail = [['boom' for i in range(len(stripped_text))] # Set the length of all the lists to the text length
            for j in range(key)] # Set the amount of lists to the key

    # Set up initial variables
    going_down = False
    row = 0
    column = 0

    for char in range(len(stripped_text)):
        # Make sure we aren't at the top/bottom of the 2d list, if so switch direction
        if row == 0 or row == (key - 1):
            going_down = not going_down

        # Set current spot to the character
        rail[row][column] = stripped_text[char]
        column += 1

        # Change rows based on which direction we're going
        if not going_down:
            row -= 1
        else:
            row += 1


    # Create new text after encryption's completed

    new_text = []

    for row in range(key):
        for column in range(len(stripped_text)):
            if rail[row][column] != "boom":
                new_text.append(rail[row][column])

    return "".join(new_text)


