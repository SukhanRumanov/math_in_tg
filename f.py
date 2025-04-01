def f(x, y, z):
    if x<=y<=z: return True
    else: return False
max_= 0
for a1 in range(1, 100):
    for a2 in range(a1, 200):
       
        k = 0
        for x in range(1, 100):
            if(not(f(5,x,30) == (f(14, x, 23))) or not((f(a1,x,a2)))):
                k+=1
        if k == 99:
            max_ = max(max_, a2-a1)
print(max_)