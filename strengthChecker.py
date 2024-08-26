import hashlib
import requests
import re
import alive_progress
import itertools
import string
import time

# Ask the user for a password to test.
userPassword = input("Please enter the password you want to test: ")

#first lets look an see if it can be broken instantly via existing password dictonaries:

#get the password hash into a state that it will be useful for comparison
password_hash = hashlib.sha1(str.encode(userPassword)).hexdigest().upper()

print(f"Password SHA1 hash: {password_hash}")

prefix = password_hash[:5]
suffix = password_hash[5:]

#primary url for haveibeenpwned
pwd_api_url = 'https://api.pwnedpasswords.com/range'

response = requests.get(f'{pwd_api_url}/{prefix}')

print("================================== DICTIONARY CHECK: HAVEIBEENPWNED ==================================")

# Check the status code of the response
if response.status_code != 200:
    print("Error checking password")
else:
    # Check if the hashed password suffix exists in the response
    for line in response.text.splitlines():
        line_suffix, count = line.split(':')
        if line_suffix == suffix:
            print(f"Password found {count} times. Please use a different password.")
            break
    else:
        print(f"Password not found. You can use this password.")
        
print("================================== MATHEMATICAL PASSWORD STRENGTH ==================================")

possible_combos = 0

#we will now check the complexity "strength" of the given password.

#does it have letters?
has_letters = re.search('[a-zA-Z]', userPassword)

if has_letters:
    possible_combos += 26
    print("Your Password Has Alphabetical Letters! Plus 26 Possible Characters!")

#does it have numbers?
has_numbers = re.search('[0-9]', userPassword)

if has_numbers:
    possible_combos += 10
    print("Your Password Has Numbers! Plus 10 Possible Characters!")

#does it have special characters?
has_specials = re.search('@_!#$%^&*()<>?/\|}{~:', userPassword)

if has_specials:
    possible_combos += 21
    print("Your Password Has Special Characters! Plus 21 Possible Characters!")
    
#the number of possible combos is the number of possible characters to the power of the length of the password
    
possible_combos = pow(possible_combos, len(userPassword))

print(f"Your password has {possible_combos} possible combinations")

iterable = string.ascii_letters + string.digits + "@_!#$%^&*()<>?/\|}{~:"

print("Start Plaintext Bruteforce: 1")
print("Start SHA1 Bruteforce: 2")
menu_choice = int(input("Input Menu Choice: "))

if menu_choice == 1:
    start_time = time.time()
    for password_length in range(1,16):
        for password in alive_progress.alive_it(itertools.permutations(iterable, password_length)):
            guess = ''.join(password)
            if guess == userPassword:
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"Your password was bruteforced in {execution_time} seconds")
elif menu_choice == 2:
    start_time = time.time()      
    for password_length in range(1,16):
        for password in alive_progress.alive_it(itertools.permutations(iterable, password_length)):
            guess = ''.join(password)
            guess_hash = hashlib.sha1(str.encode(guess)).hexdigest().upper()
            if guess_hash == password_hash:
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"Your password was bruteforced in {execution_time} seconds")