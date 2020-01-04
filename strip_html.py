with open("test.txt", 'r') as fhandle:
    for i in fhandle:
        if not 'class="word"' in i:
            continue
        print(i)
