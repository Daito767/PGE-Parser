import colorama
from colorama import Fore, Back, Style


def print_red(text: str):
	print(Fore.RED + text + Style.RESET_ALL, end='')


def print_green(text: str):
	print(Fore.GREEN + text + Style.RESET_ALL, end='')


def print_yellow(text: str):
	print(Fore.YELLOW + text + Style.RESET_ALL, end='')


def print_blue(text: str):
	print(Fore.BLUE + text + Style.RESET_ALL, end='')


def print_magenta(text: str):
	print(Fore.MAGENTA + text + Style.RESET_ALL, end='')


def print_cyan(text: str):
	print(Fore.CYAN + text + Style.RESET_ALL, end='')


def println_red(text: str):
	print(Fore.RED + text + Style.RESET_ALL)


def println_green(text: str):
	print(Fore.GREEN + text + Style.RESET_ALL)


def println_yellow(text: str):
	print(Fore.YELLOW + text + Style.RESET_ALL)


def println_blue(text: str):
	print(Fore.BLUE + text + Style.RESET_ALL)


def println_magenta(text: str):
	print(Fore.MAGENTA + text + Style.RESET_ALL)


def println_cyan(text: str):
	print(Fore.CYAN + text + Style.RESET_ALL)
