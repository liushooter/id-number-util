hid = "4103261995xxxx3197"

verify_id = str(hid)[-1]
left = hid[0:10]
right = hid[14:18]

month = range(1, 13)
day = range(1, 32)

fakes = []
for mon in month:
    for d in day:
        mm = ''
        dd = ''
        if mon < 10:
            mm = '0' + str(mon)
        else:
            mm = str(mon)

        if d < 10:
            dd = '0' + str(d)
        else:
            dd = str(d)

        mid = mm + dd
        fake = left + mid + right
        fakes.append(fake)

arr = []
for i in range(0, 17):
    a = (1 << 17 - i) % 11
    arr.append(a)

for idcard in fakes:

    a = str(idcard)[0:-1]

    check_sum = 0
    for (inx, z) in enumerate(a):
        num = int(z)
        check_sum += num * arr[inx]

    check_digit = (12 - check_sum % 11) % 11

    if check_digit == int(verify_id):
        print(idcard[10:14])
