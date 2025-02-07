import curses
import pyperclip

def generate_matrix_string(matrix):
    
    lines = []
    
    for row in matrix:
        
        line = "[" + " ".join(str(cell) for cell in row) + "]"
        lines.append(line)
        
    return "```\n" + "\n".join(lines) + "\n```"

def place_bar_mode(stdscr, matrix, rows, cols, cell_width, cr, cc):

    bar_pos = cc + 1 if cc + 1 < cols else cols - 1

    while True:

        stdscr.clear()

        for i in range(rows):

            for j in range(cols):

                cell_str = str(matrix[i][j])
                x, y = j * cell_width, i
                attr = curses.A_BOLD if cell_str == "|" else curses.A_NORMAL

                stdscr.addstr(y, x, cell_str.center(cell_width), attr)

        bar_x = bar_pos * cell_width

        for i in range(rows):

            stdscr.addch(i, bar_x, '|', curses.A_BOLD)

        stdscr.addstr(rows + 1, 0, "Bar placement mode")
        stdscr.refresh()

        key = stdscr.getch()

        if key in (curses.KEY_LEFT, curses.KEY_RIGHT):

            if key == curses.KEY_LEFT:

                if bar_pos > 1:

                    bar_pos -= 1

            elif key == curses.KEY_RIGHT:

                if bar_pos < cols - 1:

                    bar_pos += 1

        elif key in (curses.KEY_ENTER, 10, 13):

            for row in matrix:

                row.insert(bar_pos, "|")

            cols += 1

            return matrix, rows, cols

        elif key == ord('c'):

            return matrix, rows, cols

def editor(stdscr, matrix, rows, cols):

    curses.curs_set(0)
    stdscr.keypad(True)
    cell_width = 7

    cr, cc = 0, 0
    edit_buffer = matrix[cr][cc]

    while True:

        stdscr.clear()

        for i in range(rows):

            for j in range(cols):

                cell_str = str(matrix[i][j])
                x, y = j * cell_width, i
                attr = curses.A_BOLD if cell_str == "|" else curses.A_NORMAL

                if i == cr and j == cc:

                    attr |= curses.A_REVERSE

                stdscr.addstr(y, x, cell_str.center(cell_width), attr)

        stdscr.addstr(rows + 1, 0, "'esc' to clear, 'q' to quit.")
        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):

            break

        elif key == 27:

            stdscr.clear()
            stdscr.addstr(0, 0, "Press 'c' to continue, 'q' to quit, 'b' to place a bar, or 's' to copy string.")
            stdscr.refresh()

            option = stdscr.getch()
            while option not in (ord('c'), ord('q'), ord('b'), ord('s')):

                stdscr.addstr(1, 0, "Invalid option. Please press 'c', 'q', 'b', or 's'.")
                stdscr.refresh()
                option = stdscr.getch()

            if option == ord('q'):

                break

            elif option == ord('b'):

                matrix, rows, cols = place_bar_mode(stdscr, matrix, rows, cols, cell_width, cr, cc)

                if cc >= cols:

                    cc = cols - 1

                edit_buffer = matrix[cr][cc]

            elif option == ord('s'):

                matrix_str = generate_matrix_string(matrix)
                pyperclip.copy(matrix_str)
                continue

        elif key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):

            if key == curses.KEY_UP:

                cr = max(0, cr - 1)

            elif key == curses.KEY_DOWN:

                cr = min(rows - 1, cr + 1)

            elif key == curses.KEY_LEFT:

                cc = max(0, cc - 1)

            elif key == curses.KEY_RIGHT:

                cc = min(cols - 1, cc + 1)

            edit_buffer = str(matrix[cr][cc])

        elif key in (curses.KEY_ENTER, 10, 13):

            if cc < cols - 1:

                cc += 1

            elif cr < rows - 1:

                cr += 1
                cc = 0

            edit_buffer = matrix[cr][cc]

        elif 48 <= key <= 57:  # ascii codes 0 - 9

            digit = chr(key)

            if edit_buffer in ("0", "-0"):

                edit_buffer = digit

            else:

                edit_buffer += digit

            matrix[cr][cc] = edit_buffer

        elif (65 <= key <= 90) or (97 <= key <= 122) or key in (ord('_'), ord('+'), ord('-'), ord('*'), ord('/'), ord('.'), ord('^')):

            ch = chr(key)

            if edit_buffer == "0":

                edit_buffer = ch

            else:

                edit_buffer += ch

            matrix[cr][cc] = edit_buffer

        elif key in (curses.KEY_BACKSPACE, 127, 8):

            edit_buffer = edit_buffer[:-1]

            if edit_buffer == "" or edit_buffer == "-":

                edit_buffer = "0"

            matrix[cr][cc] = edit_buffer

def main():

    rows, cols = 0, 0

    while not rows and not cols:

        start = input("Enter the number of rows and columns: ").strip().lower()

        if 'x' in start:

            rows, cols = map(int, start.split('x'))

        elif ' ' in start:

            rows, cols = map(int, start.split())

        elif ', ' in start:

            rows, cols = map(int, start.split(', '))

        elif ',' in start:

            rows, cols = map(int, start.split(','))

        elif ' - ' in start:

            rows, cols = map(int, start.split(' - '))

        elif '-' in start:

            rows, cols = map(int, start.split('-'))

        else:

            print("What the hell is this format")

    matrix = [["0"] * cols for _ in range(rows)]
    curses.wrapper(editor, matrix, rows, cols)

if __name__ == "__main__":

    main()
