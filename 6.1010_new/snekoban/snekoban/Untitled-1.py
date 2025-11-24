def raph(x, num):
    list = [x]
    
    for i in range(num):
        input = list[i]
        output = input - (input**2 -2)/ (2*input)
        list.append(output)
    return list    

print(raph(0, 10))
    
    