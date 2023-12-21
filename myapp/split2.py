def split(name):
    split_text = name.split(',')
    Name = split_text[0]
    Employee_id = split_text[1]
    Company_id = split_text[2]
    print(Name,Employee_id,Company_id)
    return(Name,Employee_id,Company_id)


filename = "Ardra P,01010101,403"
split(filename)