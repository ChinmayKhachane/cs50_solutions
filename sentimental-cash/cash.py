from cs50 import get_float

change = 0;
count = 0;

while change <= 0:
    change = get_float("How much change?")

cents = round(change * 100)

while cents > 0:
    while cents >= 25:
        count += 1
        cents -= 25
    while cents >= 10:
        count += 1
        cents -= 10
    while cents >= 5:
        count += 1
        cents -= 5
    while cents >= 1:
        cents -= 1
        count += 1

print(str(count) + " coins")



