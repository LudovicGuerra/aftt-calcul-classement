# Main data

list_rank_inversed = ["B0", "B2", "B4", "B6", "C0", "C2", "C4", "C6", "D0", "D2", "D4", "D6", "E0", "E2", "E4", "E6", "NC"]  # 17
list_rank = list(reversed(list_rank_inversed))
list_win_inversed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 10, 11, 4]
list_lose_inversed = [0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 3, 3, 4, 1, 0]
list_win = list(reversed(list_win_inversed))
list_lose = list(reversed(list_lose_inversed))


def main():
    current_rank = "E6"
    rank_residu_method = residu_method(current_rank)
    rank_limberg_method = limburg_method(current_rank)


# Residu method

def residu_method(current_rank):
    last_sum_residu = 0
    target_rank = "E6"
    percentage_table_win = {}
    for i in range(-17, 0):
        percentage_table_win[i] = round((100 - 50 / 100 * ((3 / 5) ** -i) * 100) / 100, 2)
    for i in range(0, 17):
        percentage_table_win[i] = round(50 / 100 * ((3 / 5) ** i), 2)
    print(percentage_table_win)

    while True:
        list_number_victory_expected = []
        print("Target rank is: {}".format(target_rank))
        for index_rank in range(0, len(list_rank)):
            target_rank_offset = index_rank - list_rank.index(target_rank)
            list_number_victory_expected.append(percentage_table_win[target_rank_offset] * (list_win[index_rank] + list_lose[index_rank]))

        residu = [i - j for i, j in zip(list_win, list_number_victory_expected)]
        print(list_number_victory_expected)
        print("Residu is: {}".format(residu))
        print("Sum Residu is: {}".format(sum(residu)))

        if sum(residu) > 0 or (sum(residu) < 0 and abs(sum(residu)) < abs(last_sum_residu)):
            last_sum_residu = sum(residu)
            if target_rank != list_rank[-1]:
                target_rank = list_rank[list_rank.index(target_rank) + 1]
            else:
                break
        else:
            break
    final_rank = list_rank[list_rank.index(target_rank) - 1]
    print("Final rank of residu method is: {}".format(final_rank))
    return final_rank


#  Limburg/Kempen method

def limburg_method(current_rank):
    ponderation_table_win = {-4: 1, -3: 1, -2: 1, -1: 1, 0: 1, 1: 1.5, 2: 2, 3: 3, 4: 4}  # -4 to +4
    ponderation_table_lose = {-4: 4, -3: 3, -2: 2, -1: 1.5, 0: 1, 1: 1, 2: 1, 3: 1, 4: 1}
    for i in range(-17, -4):
        ponderation_table_win[i] = 1
        ponderation_table_lose[i] = 4
    for i in range(5, 18):
        ponderation_table_win[i] = 4
        ponderation_table_lose[i] = 1

    target_rank = current_rank

    while True:
        score_plus = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        score_minus = list(score_plus)

        for index_rank in range(0, len(list_lose)):
            target_rank_offset = index_rank - list_rank.index(target_rank)
            score_plus[index_rank] += ponderation_table_win[target_rank_offset] * list_win[index_rank]
            score_minus[index_rank] += ponderation_table_lose[target_rank_offset] * list_lose[index_rank]
        print(score_plus)
        print(score_minus)

        for index_rank in range(0, list_rank.index(target_rank) + 1):
            diff = score_plus[index_rank] - score_minus[index_rank]
            if diff < 0:
                print("Diff not ok ({}) for index rank of {}".format(diff, index_rank))
                for j in range(index_rank + 1, len(list_rank)):
                    if score_plus[j] >= -diff:
                        score_plus[index_rank] -= diff
                        score_plus[j] += diff
                        break
                    elif score_plus[j] < -diff:
                        score_plus[index_rank] += score_plus[j]
                        score_plus[j] = 0
                        diff = score_plus[index_rank] - score_minus[index_rank]
        print(score_plus)
        print(score_minus)
        if score_plus[list_rank.index(target_rank)] - score_minus[list_rank.index(target_rank)] >= 0:
            print("Rank {} is OK".format(list_rank[list_rank.index(target_rank)]))
            target_rank = list_rank[list_rank.index(target_rank) + 1]
        else:
            print("Rank {} is BAD".format(list_rank[list_rank.index(target_rank)]))
            final_rank = list_rank[list_rank.index(target_rank) - 1]
            print("Final rank of limburg method is: {}".format(final_rank))
            return final_rank


if __name__ == "__main__":
    main()
