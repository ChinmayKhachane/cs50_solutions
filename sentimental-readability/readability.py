from cs50 import get_string

text = get_string("Enter your text: ")

let = 0;
sen = 0;
word = 0;

for i in range(len(text)):
    if(text[i].isalpha()):
        let+=1
    if(text[i] == " "):
        word+=1
    if(text[i] == "." or text[i] == "!" or text[i] == "?"):
        sen+=1

word+=1

L = (let / word) * 100
S = (sen / word) * 100
score = round(0.0588 * L - 0.296 * S -15.8)

if(score > 16):
    print("Grade 16+")
elif(score < 1):
    print("Before Grade 1")
else:
    print("Grade " + str(score))



