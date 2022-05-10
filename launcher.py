import multiprocessing as mp
from worker_module import worker
import pathlib
import os

''' 
    takes path to executable (string)
    returns Process object
'''

def init_worker(executable, pipe_read, pipe_write):
    p = mp.Process(target=worker, args=(executable, pipe_read, pipe_write))
    return p


''' 
    takes path to the executable and number of workers
    returns array of Process objects and two arrays of file descriptors
'''

def init_workers(path_to_executable, number): 
    workers = []
    input_fds = []
    output_files = []
    for i in range(0, number): 
        output_file = os.open("worker"+ str(i) + ".output", os.O_CREAT | os.O_TRUNC | os.O_WRONLY)

        r, w = os.pipe()
        worker_process = init_worker(path_to_executable, r, output_file)

        workers.append(worker_process)
        input_fds.append(w)
        output_files.append(output_file)

    return workers, input_fds, output_files


if __name__ == "__main__":
    workers, input_fds, output_files = init_workers("echo.py", 2)

    for p in workers:
        p.start()            

    for fd in input_fds:
        for i in range(0, 10):
            os.write(fd, (str(i) + "\n").encode('utf-8'));

    for p in workers:
        p.join()

    for fd in input_fds:
        os.close(fd)

    for fd in output_files:
        os.close(fd)
