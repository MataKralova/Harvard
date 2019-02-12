# Verifies if credit card number is (syntactically) valid

print("Number: ", end="")
n = int(input())

while n < 1:
    print("Retry: ", end="")
    n = input()

mod0 = n % 10  # accesses ones
mod1 = n % 100  # accesses tens
mod2 = n % 1000  # accesses hundreds
mod3 = n % 10000  # accesses thousands
mod4 = n % 100000
mod5 = n % 1000000
mod6 = n % 10000000
mod7 = n % 100000000
mod8 = n % 1000000000
mod9 = n % 10000000000
mod10 = n % 100000000000
mod11 = n % 1000000000000
mod12 = n % 10000000000000
mod13 = n % 100000000000000
mod14 = n % 1000000000000000
mod15 = n % 10000000000000000

res1 = (mod1 - mod0) // 10  # accesses 2nd digit from end
res2 = (mod3 - mod2) // 1000  # accesses 4th digit from end
res3 = (mod5 - mod4) // 100000
res4 = (mod7 - mod6) // 10000000
res5 = (mod9 - mod8) // 1000000000
res6 = (mod11 - mod10) // 100000000000
res7 = (mod13 - mod12) // 10000000000000  # accesses 14th digit from end
res8 = (mod15 - mod14) // 1000000000000000  # accesses 16th digit from end

RES1 = res1 * 2
RES2 = res2 * 2
RES3 = res3 * 2
RES4 = res4 * 2
RES5 = res5 * 2
RES6 = res6 * 2
RES7 = res7 * 2
RES8 = res8 * 2

# sums the multiplied digits
dig = RES1 // 10 + RES1 % 10 + RES2 // 10 + RES2 % 10 + RES3 // 10 + RES3 % 10 + RES4 // 10 + RES4 % 10 \
    + RES5 // 10 + RES5 % 10 + RES6 // 10 + RES6 % 10 + RES7 // 10 + RES7 % 10 + RES8 // 10 + RES8 % 10

# adds sum of multiplied digits to sum of unmultiplied digits
fin = dig + mod0 + ((mod2 - mod1) // 100) + (mod4 - mod3) // 10000 + (mod6 - mod5) // 1000000 \
    + (mod8 - mod7) // 100000000 + (mod10 - mod9) // 10000000000 + (mod12 - mod11) // 1000000000000 \
    + (mod14 - mod13) // 100000000000000

if fin % 10 == 0:
    if (mod14 - mod12) // 10000000000000 == 34 or (mod14 - mod12) // 10000000000000 == 37:
        print("AMEX")
    elif (mod15 - mod13) // 100000000000000 == 51 or (mod15 - mod13) // 100000000000000 == 52 \
            or (mod15 - mod13) // 100000000000000 == 53 or (mod15 - mod13) // 100000000000000 == 54 \
            or (mod15 - mod13) // 100000000000000 == 55:
        print("MASTERCARD")
    else:
        print("VISA")
else:
    print("INVALID")