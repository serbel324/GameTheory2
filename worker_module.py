import os

def worker(executable, input_fd, output_file):
    print(f"Worker {os.getpid()} started")
    os.dup2(input_fd, 0)
    os.dup2(output_file, 1)
    os.execl(executable, executable)
    os._exit(1)
