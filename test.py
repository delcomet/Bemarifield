def update_score(player, score):
    fr = open("score.txt", "r")
    file = fr.readlines()
    name_list = eval(file[0])
    value_list = eval(file[1])
    iteration = 0
    for a in name_list:
        if iteration >= len(value_list):
            return
        if score > value_list[iteration]:
            value_list.insert(iteration, score)
            name_list.insert(iteration, player)
            del value_list[-1]
            del name_list[-1]

            fw = open("score.txt", "w")
            fw.writelines([str(name_list), "\n", str(value_list)])
            fw.close()
            fr.close()
            print(value_list, name_list)
            return
        else:
            iteration += 1

    print(value_list, name_list)

update_score("homo", 1000)
