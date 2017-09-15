"""
A little script to get and properly format questions for quizzes, homework,
etc.
"""

DELIM = '`'
CORR_MARK = '^'

def ask(msg):
    print(msg, end='')
    ans = input()
    return ans.strip()

def ask_int(msg):
    ans = "NAN"
    while not ans.isdigit():
        ans = ask(msg)
    return ans

def add_item(item):
    return item + DELIM

answers = []

chap = ask_int("Enter chapter # for question: ")
section = ask_int("Enter section # for question: ")
question = ask("Enter question: ")
correct = ask("Enter correct answer (we will randomize for you!): ")
correct = CORR_MARK + correct
answers.append(correct)

new_bad = ""
while True:
    new_bad = ask("Enter a wrong answer (blank to stop entering): ")
    if len(new_bad) < 1:
        break
    else:
        answers.append(new_bad)

s = ""
s += add_item(chap)
s += add_item(section)
s += add_item(question)
for answer in answers:
    s += add_item(answer)

s = s[0:-1]
print(s)

