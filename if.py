#!/usr/bin/python
# Filename : if.py

number=23
value = True
while value:
    guess = int(raw_input('Enter a integer:'))
    if guess==number:
        value = False
        print('guess it')
    elif guess<number:
        print('guess wrong, less')
    else:
        print('guess wrong, more')
