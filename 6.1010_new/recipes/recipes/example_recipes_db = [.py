def combinations(list):
    input ={list[0]}
    for num in list[1:]:
        for input_num in input:
            out = set()
            
            out.update([input_num + num, ])
            