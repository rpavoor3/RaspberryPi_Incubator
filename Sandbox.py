

truth = 0.339

low = 0.28
high = 0.4

######################

count = 0
x = (high + low) / 2

while (count < 5):
    count += 1
    if (x < truth):
        x += ((high - low) / (pow(2,(count+1))))
    else:
        x -= ((high - low) / (pow(2,(count+1))))

print(x)
