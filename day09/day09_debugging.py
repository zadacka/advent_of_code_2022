from day09 import calculate_tail_positions, print_tail_positions

if __name__ == '__main__':
    tps = calculate_tail_positions('day09_real_input.txt', length=10)
    print_tail_positions(tps)