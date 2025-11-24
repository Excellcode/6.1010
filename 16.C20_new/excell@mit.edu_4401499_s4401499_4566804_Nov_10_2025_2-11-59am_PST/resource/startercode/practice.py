def max_val(t,visited=None): 
    """ t, tuple or list
        Each element of t is either an int, a tuple, or a list
        No tuple or list is empty
        Returns the maximum int in t or (recursively) in an element of t """ 
    if visited is None:
        visited = []
    
    for i in t:
        try:
            if len(i) != 0:
                max_val(i, visited)
        except:
            visited.append(i)
            
    return max(visited)
                


print(max_val((5, (1,2),[[[1],[2]]]))) 
# returns 5.
print(max_val((5, (1,2), [[[[1],[9]], 12], 14])))
#returns 9.