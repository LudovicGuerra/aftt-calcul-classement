# Methode Vlaams Brabant
Vb = 6  # Points gagne par victoire
Db = 5  # Point persu par défaite
Nb = 2  # Facteur de bonus en cas de vitoire contre un jour mieux classé
Mb = 2  # Facteur de malus en cas de vitoire contre un jour moins bien classé
nb_game_ratio = 1
nb_point_earn_ratio = 1

list_rank = ["B0", "B2", "B4", "B6", "C0", "C2", "C4", "C6", "D0", "D2", "D4", "D6", "E0", "E2", "E4", "E6",
             "NC"]  # 17 rank
our_rank = "E6"
list_win = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 10, 11, 4]
list_lose = [0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 3, 3, 4, 1, 0]

nb_point_add = 0
index_rank = 0
point_earn = 0
point_lose = 0
total_point = 0
final_update = False

update_pivot = True
Pn = 0
Pn1 = 0
number_loop = 0
nb_game = sum(list_win)
print("Nb game: {}".format(nb_game))
while update_pivot:

    for win, lose in zip(list_win, list_lose):
        # Win
        d = list_rank.index(our_rank) - index_rank
        print("Value d: {}".format(d))
        if d <= 0:
            point_earn = Vb / (2 ** (-d))
        elif d > 0:
            point_earn = Vb * (1 + d * Nb)

        if d >= 0:
            point_lose = Db / (2 ** d)
        elif d < 0:
            point_lose = Db * (1 - d * Mb)

        print("Point earn: {}".format(point_earn))
        print("Point lose: {}".format(point_lose))

        sum_point_earn = int(point_earn * win)
        sum_point_lose = int(point_lose * lose)
        total_point = int(sum_point_earn + sum_point_lose)
        print("Total point: {}".format(total_point))
        index_rank += 1
    index_rank = 0

    # Calcule pivot
    pivot = 0  # 0: No change, 1: Up, 2: Down
    if nb_game <= 4 * nb_game_ratio:
        pivot = 2
    elif nb_game > 4 * nb_game_ratio and nb_game <= 16 * nb_game_ratio:
        limit_up = -nb_game * nb_game_ratio * (1 / 5) + 24 / 5  # y = -1/5x+24/5
        limit_down = -limit_up
        print("Limit up:{}".format(limit_up))
        if total_point > limit_up:
            pivot = 1
        elif total_point < limit_down:
            pivot = 2
        else:
            pivot = 0
    elif nb_game > 16 *nb_game_ratio:
        limit_up = 1.5*nb_point_earn_ratio
        limit_down = -limit_up
        if total_point > limit_up:
            pivot = 1
        elif total_point < limit_down:
            pivot = 2
        else:
            pivot = 0
    print("Pivot: {}".format(pivot))

    if number_loop == 0:
        if pivot == 0:
            update_pivot = False
    if number_loop > 0:
        if pivot != Pn:
            update_pivot = False
    if number_loop == 0:
        Pn1 = total_point
    else:
        Pn = Pn1
        Pn1 = total_point
    if not update_pivot and Pn+Pn1 > 0:
        final_update = True
    if not update_pivot and Pn+Pn1 < 0:
        final_update = False

    number_loop += 1
    if update_pivot or (not update_pivot and final_update):
        our_rank = list_rank[list_rank.index(our_rank) - 1]
    print("Rank: {}\r\n\r\n\r\n".format(our_rank))

    #time.sleep(1)

print("Our rank is: {}".format(our_rank))