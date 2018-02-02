import subprocess as sp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-num_balls", "-n", type=int, required=False,
                    default=4, help="")
parser.add_argument("-num_reps", "-r", type=int, required=False,
                    default=100, help="")
args = parser.parse_args()

template = ('python visual_pygame.py -n {n} -p 0 -name {name} -c {c}')

processes = []
for i in range(args.num_reps):  
    name = str(args.num_balls) + str(i) + str('c0')
    cmd = template.format(n=args.num_balls, name=name, c=0)
    cmd = cmd.split()
    process = sp.Popen(cmd, stdout=sp.PIPE)
    processes.append(process)

    if (i % 50 == 0):
        for p in processes:
            p.wait()
        processes = []



