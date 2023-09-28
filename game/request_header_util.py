




if __name__=="__main__":
    file = open('request_header_paste.txt', 'r')
    lines = file.readlines()
    line_count = 1
    map = {}
    key = ""
    value = ""
    for line in lines:
        line = line.strip('\n')
        if line_count % 2 != 0:
            key = line[0:-1]
        else:
            value = line
            map[key] = value
        line_count = line_count + 1
    print(map)
