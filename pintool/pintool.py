#!/usr/bin/env python3

import argparse
import asyncio
import string
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from .pin import pin

def get_args():
	
	parser = argparse.ArgumentParser(description="Program for playing with Pin")
	parser.add_argument(
		"-d",
		"--detect",
		action="store_true",
		default=False,
		help="Detect the password length. For example -d -l 40, with 40 characters"
	)
	parser.add_argument("-l", dest="len", type=int, default=10, help="Length of password")
	parser.add_argument(
		"-c",
		"--charset",
		default="default",
		help=(
		"Charset definition for brute force"
		" (default, default2, lower, upper, digit, hex, punct, print)"
		)
	)
	parser.add_argument(
		"-b",
		"--chars",
		"--characters",
		dest="characters",
		default="",
		help="Add characters for the charset. For example, -b _-"
	)
	parser.add_argument(
		"-a", "--arch", default="64", help="Program architecture", choices=["32", "64"]
	)
	parser.add_argument(
		"-i",
		"--init",
		"--init-pass",
		dest="init_pass",
		default="",
		help="Initial password characters. For example, -i CTF{"
	)
	parser.add_argument("-s", "--symbol", default="-", help="Symbol used as password placeholder")
	parser.add_argument(
		"-e",
		"--expression",
		default="!= 0",
		help=(
		"Difference between instructions that are successful or not. "
		"For example: -e '== -12', -e '=> 900', -e '<= 17' or -e '!= 32'"
		)
	)
	parser.add_argument(
		"-r",
		"--reverse",
		action="store_true",
		default=False,
		help="Reverse order, bruteforcing starting from the last character"
	)
	parser.add_argument(
		"-u",
		"--unordered",
		"--non-ascending",
		dest="ascending",
		action="store_false",
		default=True,
		help="Target program doesn't check chars in ascending order"
	)
	parser.add_argument(
		"-g",
		"--argv",
		dest="use_argv",
		action="store_true",
		default=False,
		help="Pass argument via command-line arguments instead of stdin."
	)
	parser.add_argument("filename", type=Path)
	parser.add_argument("additional_args", nargs="*")
	
	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit()
	
	return parser.parse_args()

def get_charset(charset_str, additional):
	charsets = {
		"default":
		string.ascii_lowercase + "_" + string.digits + "{}" + string.ascii_uppercase +
		string.punctuation.translate(str.maketrans("", "", "_{}")),
		"default2":
		string.ascii_lowercase + "_" + string.digits + "{}",
		"lower":
		string.ascii_lowercase,
		"upper":
		string.ascii_uppercase,
		"digit":
		string.digits,
		"hex":
		string.digits + "abcdef",
		"punct":
		string.punctuation,
		"print":
		string.printable
	}
	
	return "".join(charsets[name] for name in charset_str.split(",")) + "".join(additional)

def get_cmp_func(expression):
	comparison, number = expression.split(" ")
	number = int(number)
	try:
		cmp_func = {
			"!=": lambda diff: diff != number,
			"<=": lambda diff: diff <= number,
			">=": lambda diff: diff >= number,
			"=>": lambda diff: diff >= number,
			"==": lambda diff: diff == number,
			">": lambda diff: diff > number,
			"<": lambda diff: diff < number,
		}[comparison]
	except KeyError:
		print("Unknown value for -e option")
		sys.exit(1)
	return cmp_func

async def detect_length(filename, inscount_file, max_len, symbol="-", argv=False):
	initial = None
	for i in range(1, max_len + 1):
		password = symbol * i
		inscount = await pin(filename, inscount_file, password, argv)
		
		if initial is None:
			initial = inscount
		
		print(f"{password} = with {i} characters difference {inscount - initial} instructions")

def get_password(password, char, i):
	return password[:i] + char + password[i + 1:]

async def solve(
	filename,
	arch,
	pass_len,
	charset,
	cmp_func,
	symbol="-",
	init_pass="",
	additional_args=None,
	reverse=False,
	ascending=True,
	use_argv=False,
):
	if additional_args is None:
		additional_args = []
	
	with TemporaryDirectory() as tempdir:
		semaphore = asyncio.Semaphore(5)  # rate limit
		
		async def helper(initial, val, char):
			async with semaphore:
				inscount = await pin(
					filename, arch, val, additional_args, use_argv, f"{tempdir}/inscount{char}.out"
				)
				diff = inscount - initial
				print(f"{val} = {inscount} difference {diff} instructions")
				return cmp_func(diff), char
		
		init_len = len(init_pass)
		password = init_pass + symbol * (pass_len - init_len)
		
		while True:
			r = range(init_len, pass_len)
			if reverse:
				r = reversed(r)
			
			for i in r:
				# continue if current char is already filled in
				if password[i] != symbol:
					continue
				
				#get initial instruction count
				initial = await pin(
					filename, arch, get_password(password, symbol, i), additional_args, use_argv,
					f"{tempdir}/inscount.out"
				)
				
				coros = [
					asyncio.create_task(helper(initial, get_password(password, char, i), char))
					for char in charset
				]
				
				for coro in asyncio.as_completed(coros):
					success, char = await coro
					if success:
						for coro2 in coros:
							coro2.cancel()
						password = get_password(password, char, i)
						print(password)
						break
				else:
					if ascending:
						print("Password not found, try changing charsets")
						sys.exit(1)
					else:  # if the password is checked in a non-ascending order, we try the next index
						continue
				# valid character was found
				break
			
			# all password characters are filled in
			if symbol not in password:
				# allow task cancellations to be processed
				await asyncio.sleep(0)
				return password

def cleanup():
	path = Path("pin.log")
	if path.exists():
		path.unlink()

def main():
	args = get_args()
	
	symbol = args.symbol
	charset = get_charset(args.charset, args.characters)
	
	filename = args.filename.resolve()
	if not filename.exists():
		print("File does not exist.")
		sys.exit(1)
	filename = str(filename)
	
	init_pass = args.init_pass
	pass_len = args.len
	if len(init_pass) >= pass_len:
		print("The length of the initial password must be less than the password length.")
		sys.exit(1)
	
	if len(symbol) > 1:
		print("Only one symbol is allowed.")
		sys.exit(1)
	
	cmp_func = get_cmp_func(args.expression.strip())
	
	arch = args.arch
	if arch not in ["32", "64"]:
		print("Unknown architecture")
		sys.exit(1)
	
	try:
		
		if args.detect:
			asyncio.run(detect_length(filename, arch, pass_len, symbol, args.use_argv))
		else:
			password = asyncio.run(
				solve(
				filename, arch, pass_len, charset, cmp_func, symbol, init_pass,
				args.additional_args, args.reverse, args.ascending, args.use_argv
				)
			)
			print("Password:", password)
	finally:
		cleanup()

if __name__ == "__main__":
	main()
