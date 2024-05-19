import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Угадай число")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

font = pygame.font.SysFont(None, 48)
font_1 = pygame.font.SysFont(None, 40)

MIN_NUMBER = 0
MAX_NUMBER = 100
random_number = random.randint(MIN_NUMBER, MAX_NUMBER)

guess_text = ''
message_text = font_1.render("Программа загадала целое число от 0 до 100.", True, BLUE)
message_text_1 = font_1.render("Попробуйте угадать, введя целое число и нажав Enter", True, BLUE)
result_text = font.render("", True, BLACK)
quit_text = font.render("Нажмите Q, чтобы выйти", True, BLACK)
restart_text = font.render("Нажмите R, чтобы сыграть ещё", True, BLACK)
game_over = False
correct_guesses = 0
guessed_numbers = []
scroll_offset = 0
scroll_speed = 5

numbers_per_row = 8

def draw_window():
    WIN.fill(WHITE)

    WIN.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, 50))
    guess_surface = font.render(guess_text, True, BLACK)
    WIN.blit(message_text_1, (WIDTH // 2 - message_text.get_width() // 1.65, 100))
    guess_surface = font.render(guess_text, True, BLACK)
    WIN.blit(guess_surface, (WIDTH // 2 - guess_surface.get_width() // 2, 150))
    WIN.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 250))
    if game_over:
        WIN.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 350))
        WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 400))
    else:
        guesses_text = font.render(f"Угадано: {correct_guesses}", True, BLACK)
        WIN.blit(guesses_text, (WIDTH // 2 - guesses_text.get_width() // 2, 350))

        rows = (len(guessed_numbers) - 1) // numbers_per_row + 1
        start_row = scroll_offset // numbers_per_row
        end_row = min(start_row + (HEIGHT - 450) // (font.get_height() + 10), rows)

        label_text = font.render("Числа, которые вы уже ввели:", True, BLACK)
        WIN.blit(label_text, (WIDTH // 2 - label_text.get_width() // 2, 400))

        y_pos = 450
        for row in range(start_row, end_row):
            row_numbers = guessed_numbers[row * numbers_per_row: (row + 1) * numbers_per_row]
            row_text = font.render(f"{', '.join(map(str, row_numbers))}", True, BLACK)
            WIN.blit(row_text, (WIDTH // 2 - row_text.get_width() // 2, y_pos))
            y_pos += font.get_height() + 10

    pygame.display.update()

def main():
    global guess_text, result_text, game_over, random_number, correct_guesses, guessed_numbers, scroll_offset

    running = True
    while running:
        draw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            guess_number = int(guess_text)
                            if guess_number < 0 or guess_number > 100:
                                result_text = font.render("Введите число от 0 до 100", True, RED)
                                guess_text = ''
                            elif guess_number in guessed_numbers:
                                result_text = font.render("Вы уже вводили это число", True, RED)
                                guess_text = ''
                            else:
                                guessed_numbers.append(guess_number)

                                if guess_number == random_number:
                                    result_text = font.render(f'Вы угадали! Это число {random_number}!', True, GREEN)
                                    guess_text = ''
                                    game_over = True
                                    correct_guesses += 1
                                elif guess_number < random_number:
                                    result_text = font.render(f'Загаданное число больше {guess_number}', True, RED)
                                    guess_text = ''
                                else:
                                    result_text = font.render(f'Загаданное число меньше {guess_number}', True, RED)
                                    guess_text = ''
                        except ValueError:
                            result_text = font.render("Введите корректное число", True, RED)
                            guess_text = ''

                    elif event.key == pygame.K_BACKSPACE:
                        guess_text = guess_text[:-1]
                    else:
                        guess_text += event.unicode

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        random_number = random.randint(MIN_NUMBER, MAX_NUMBER)
                        result_text = font.render("", True, BLACK)
                        game_over = False
                        guessed_numbers = []
                        scroll_offset = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and event.button == 4:
                    scroll_offset -= scroll_speed
                    if scroll_offset < 0:
                        scroll_offset = 0
                elif not game_over and event.button == 5:
                    scroll_offset += scroll_speed
                    max_scroll_offset = (len(guessed_numbers) - 1) // numbers_per_row * numbers_per_row
                    if scroll_offset > max_scroll_offset:
                        scroll_offset = max_scroll_offset

    pygame.quit()


if __name__ == '__main__':
    main()
