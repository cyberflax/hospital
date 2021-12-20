def fun(n):
    for i in range(0,n):
        for j in range(i+1):
            print(' ',endwith=' ')
        for j in range(n-i):
            print('*',endwith=' ')
        print()