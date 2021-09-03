
def inline(list, add=None):

    new_list = [[list[i],list[i+1]] for i in range(0,len(list),2)] if len(list)%2 == 0 else [[list[i],list[i+1]] for i in range(0,len(list) - 1,2)] + [[list[len(list)-1]]]
    if add:
        new_list += add

    return new_list
