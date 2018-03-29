import logging

# create debug
logging.basicConfig(level=logging.DEBUG)

debug = logging.getLogger(__name__)
debug.setLevel(logging.ERROR)

# Main data

# Personal Data
# current_rank = "E6"
# Ludo first pass
# list_win_inversed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 10, 11, 4]
# list_lose_inversed = [0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 3, 3, 4, 1, 0]

# Ludo second pass
# list_win_inversed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 9, 10, 3]
# list_lose_inversed = [0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 0, 3, 3, 4, 1, 0]

# Alain fraiture first pass
current_rank = "D4"
list_win_inversed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 11, 10, 17, 6, 6, 1]
list_lose_inversed = [0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 6, 3, 9, 10, 0, 0, 0, 0]

# Untouched data
list_rank_inversed = ["A", "B0", "B2", "B4", "B6", "C0", "C2", "C4", "C6", "D0", "D2", "D4", "D6", "E0", "E2", "E4", "E6", "NC"]  # 18
list_rank = list(reversed(list_rank_inversed))
list_win = list(reversed(list_win_inversed))
list_lose = list(reversed(list_lose_inversed))


def main():
    debug.critical("Residu method:\r\n")
    rank_residu_method = residu_method(current_rank)
    debug.critical("Limburg method:\r\n")
    rank_limberg_method = limburg_method(current_rank)
    debug.critical("Vlaams method:\r\n")
    rank_vlaams_method = vlaams_method(current_rank)
    rank_majority_method = majority_method(rank_residu_method, rank_limberg_method, rank_vlaams_method)
    debug.critical("Rank by residu method is: {}".format(rank_residu_method))
    debug.critical("Rank by limberg method is: {}".format(rank_limberg_method))
    debug.critical("Rank by vlaams method is: {}".format(rank_vlaams_method))


# Majority method
def majority_method(first_rank, second_rank, third_rank):
    pass


# Residu method

def residu_method(current_rank):
    last_sum_residu = 0
    target_rank = "E6"
    percentage_table_win = {}
    for i in range(-18, 0):
        percentage_table_win[i] = round((100 - 50 / 100 * ((3 / 5) ** -i) * 100) / 100, 2)
    for i in range(0, 18):
        percentage_table_win[i] = round(50 / 100 * ((3 / 5) ** i), 2)
    debug.debug(percentage_table_win)

    while True:
        list_number_victory_expected = []
        debug.debug("Target rank is: {}".format(target_rank))
        for index_rank in range(0, len(list_rank)):
            target_rank_offset = index_rank - list_rank.index(target_rank)
            list_number_victory_expected.append(percentage_table_win[target_rank_offset] * (list_win[index_rank] + list_lose[index_rank]))

        residu = [i - j for i, j in zip(list_win, list_number_victory_expected)]
        debug.debug(list_number_victory_expected)
        debug.debug("Residu is: {}".format(residu))
        debug.error("Sum Residu is: {}".format(sum(residu)))

        if sum(residu) > 0 or (sum(residu) < 0 and abs(sum(residu)) < abs(last_sum_residu)):
            last_sum_residu = sum(residu)
            if target_rank != list_rank[-1]:
                target_rank = list_rank[list_rank.index(target_rank) + 1]
            else:
                break
        else:
            debug.error("Working rank: {}".format(target_rank))
            debug.error("Residu is: {}".format(residu))
            break
    final_rank = list_rank[list_rank.index(target_rank) - 1]
    debug.debug("Final rank of residu method is: {}".format(final_rank))
    return final_rank


#  Limburg/Kempen method
def limburg_method(current_rank):
    ponderation_table_win = {-4: 1, -3: 1, -2: 1, -1: 1, 0: 1, 1: 1.5, 2: 2, 3: 3, 4: 4}  # -4 to +4
    ponderation_table_lose = {-4: 4, -3: 3, -2: 2, -1: 1.5, 0: 1, 1: 1, 2: 1, 3: 1, 4: 1}
    for i in range(-18, -4):
        ponderation_table_win[i] = 1
        ponderation_table_lose[i] = 4
    for i in range(5, 19):
        ponderation_table_win[i] = 4
        ponderation_table_lose[i] = 1

    target_rank = current_rank

    while True:
        score_plus = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        score_minus = list(score_plus)

        for index_rank in range(0, len(list_lose)):
            target_rank_offset = index_rank - list_rank.index(target_rank)
            score_plus[index_rank] += ponderation_table_win[target_rank_offset] * list_win[index_rank]
            score_minus[index_rank] += ponderation_table_lose[target_rank_offset] * list_lose[index_rank]
        debug.debug(score_plus)
        debug.debug(score_minus)

        for index_rank in range(0, list_rank.index(target_rank) + 1):
            diff = score_plus[index_rank] - score_minus[index_rank]
            if diff < 0:
                debug.error("Working rank: {}".format(target_rank))
                debug.error("Diff not ok ({}) for index rank of {}".format(diff, index_rank))
                debug.error(score_plus)
                debug.error(score_minus)
                for j in range(index_rank + 1, len(list_rank)):
                    if score_plus[j] >= -diff:
                        score_plus[index_rank] -= diff
                        score_plus[j] += diff
                        break
                    elif score_plus[j] < -diff:
                        score_plus[index_rank] += score_plus[j]
                        score_plus[j] = 0
                        diff = score_plus[index_rank] - score_minus[index_rank]
                debug.error(score_plus)
                debug.error(score_minus)
        debug.debug(score_plus)
        debug.debug(score_minus)
        if score_plus[list_rank.index(target_rank)] - score_minus[list_rank.index(target_rank)] >= 0:
            debug.debug("Rank {} is OK".format(list_rank[list_rank.index(target_rank)]))
            target_rank = list_rank[list_rank.index(target_rank) + 1]
        else:
            debug.debug("Rank {} is BAD".format(list_rank[list_rank.index(target_rank)]))
            final_rank = list_rank[list_rank.index(target_rank) - 1]
            debug.debug("Final rank of limburg method is: {}".format(final_rank))
            return final_rank


# Methode Vlaams Brabant
def vlaams_method(current_rank):
    Vb = 6  # Points gagne par victoire
    Db = 5  # Point persu par défaite
    Nb = 2  # Facteur de bonus en cas de vitoire contre un jour mieux classé
    Mb = 2  # Facteur de malus en cas de vitoire contre un jour moins bien classé
    nb_game_ratio = 1
    nb_point_earn_ratio = 1

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
    last_pivot = 0
    nb_game = sum(list_win)
    debug.debug("Nb game: {}".format(nb_game))
    our_rank = current_rank
    while update_pivot:

        for win, lose in zip(list_win, list_lose):
            # Win
            debug.debug("Win: {}, Lose: {}".format(win, lose))
            d = index_rank - list_rank.index(our_rank)
            debug.debug("Value d: {}".format(d))
            if d <= 0:
                point_earn = Vb / (2 ** (-d))
            elif d > 0:
                point_earn = Vb * (1 + d * Nb)

            if d >= 0:
                point_lose = Db / (2 ** d)
            elif d < 0:
                point_lose = Db * (1 - d * Mb)

            debug.debug("Point earn: {}".format(point_earn))
            debug.debug("Point lose: {}".format(point_lose))

            sum_point_earn = int(point_earn * win)
            sum_point_lose = -int(point_lose * lose)
            total_point += int(sum_point_earn + sum_point_lose)
            index_rank += 1
        index_rank = 0
        debug.error("Total point earn: {}".format(total_point))

        # Calcule pivot
        pivot = 0  # 0: No change, 1: Up, 2: Down
        if nb_game <= 4 * nb_game_ratio:
            pivot = 2
        elif nb_game > 4 * nb_game_ratio and nb_game <= 16 * nb_game_ratio:
            limit_up = -nb_game * nb_game_ratio * (1 / 5) + 24 / 5  # y = -1/5x+24/5
            limit_down = -limit_up
            if total_point > limit_up:
                pivot = 1
            elif total_point < limit_down:
                pivot = 2
            else:
                pivot = 0
        elif nb_game > 16 * nb_game_ratio:
            limit_up = 1.5 * nb_point_earn_ratio
            limit_down = -limit_up
            if total_point > limit_up:
                pivot = 1
            elif total_point < limit_down:
                pivot = 2
            else:
                pivot = 0
        debug.error("Pivot: {}".format(pivot))

        if number_loop == 0:
            Pn1 = total_point
            last_pivot = pivot
            if pivot == 0:
                update_pivot = False
        if number_loop > 0:
            Pn = Pn1
            Pn1 = total_point
            if pivot == 1:
                if pivot == last_pivot:
                    pass
                elif pivot != last_pivot:
                    update_pivot = False

            elif pivot == 0 or pivot == 2:
                if pivot != last_pivot:
                    update_pivot = False


        if not update_pivot and Pn + Pn1 > 0:
            final_update = True
        if not update_pivot and Pn + Pn1 < 0:
            final_update = False

        number_loop += 1
        total_point = 0
        if update_pivot or (not update_pivot and final_update):
            if pivot == 1:
                our_rank = list_rank[list_rank.index(our_rank) + 1]
            elif pivot==2:
                our_rank = list_rank[list_rank.index(our_rank) - 1]
        debug.error("Rank: {}".format(our_rank))

        # time.sleep(1)

    debug.debug("Our rank is: {}".format(our_rank))
    return our_rank


if __name__ == "__main__":
    main()
