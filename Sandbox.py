

truth = 0.315

low = 0
high = 3.3

######################

count = 0
x = (high - low) / 2

while (count < 16):
    count += 1
    if (x < truth):
        x += ((high - low) / (pow(2,(count+1))))
    else:
        x -= ((high - low) / (pow(2,(count+1))))

print(x)
