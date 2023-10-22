import asyncio
import subprocess
from pathlib import Path

PIN = Path("/opt/pin/pin").expanduser()
INSCOUNT32 = Path("/opt/pin/source/tools/ManualExamples/obj-ia32/inscount0.so").expanduser()
INSCOUNT64 = Path("/opt/pin/source/tools/ManualExamples/obj-intel64/inscount0.so").expanduser()

def _show_log():
	log_file = Path("pin.log")
	if log_file.exists():
		with log_file.open(encoding="utf-8") as f:
			# skip version and copyright lines
			f.readline()
			f.readline()
			print(f.read())

def _read_output(out_file):
	out_path = Path(out_file)
	with out_path.open(encoding="utf-8") as f:
		output = f.read()
	return int(output.partition(" ")[2])

def pin_sync(filename, arch, val, additional_args=None, use_argv=False, out_file="inscount.out"):
	if additional_args is None:
		additional_args = []
	
	inscount = {"64": INSCOUNT64, "32": INSCOUNT32}[arch]
	
	if use_argv:
		subprocess.run(
			[PIN, "-t", inscount, "-o", out_file, "--", filename, *additional_args, val],
			check=False,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL
		)
	else:
		subprocess.run(
			[PIN, "-t", inscount, "-o", out_file, "--", filename, *additional_args],
			input=val.encode() + b"\n",
			check=False,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL
		)
	
	_show_log()
	return _read_output(out_file)

async def pin(filename, arch, val, additional_args=None, use_argv=False, out_file="inscount.out"):
	if additional_args is None:
		additional_args = []
	
	inscount = {"64": INSCOUNT64, "32": INSCOUNT32}[arch]
	
	if use_argv:
		process = await asyncio.create_subprocess_exec(
			PIN,
			"-t",
			inscount,
			"-o",
			out_file,
			"--",
			filename,
			*additional_args,
			val,
			stdout=asyncio.subprocess.DEVNULL,
			stderr=asyncio.subprocess.DEVNULL
		)
		await process.communicate()
	else:
		process = await asyncio.create_subprocess_exec(
			PIN,
			"-t",
			inscount,
			"-o",
			out_file,
			"--",
			filename,
			*additional_args,
			stdin=asyncio.subprocess.PIPE,
			stdout=asyncio.subprocess.DEVNULL,
			stderr=asyncio.subprocess.DEVNULL
		)
		await process.communicate(val.encode() + b"\n")
	
	_show_log()
	return _read_output(out_file)
