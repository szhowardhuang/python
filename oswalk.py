import os, sys, time

def calc_progress(progress, root, dirs):
    prog_start, prog_end, prog_slice = 0.0, 1.0, 1.0

    current_progress = 0.0
    parent_path, current_name = os.path.split(root)
    data = progress.get(parent_path)
    if data:
        prog_start, prog_end, subdirs = data
        i = subdirs.index(current_name)
        prog_slice = (prog_end - prog_start) / len(subdirs)
        current_progress = prog_slice * i + prog_start

        if i == (len(subdirs) - 1):
            del progress[parent_path]

    if dirs:
        progress[root] = (current_progress, current_progress+prog_slice, dirs)

    return current_progress

def walk(start_root):
    progress = {}
    print 'Starting with {start_root}'.format(**locals())

    for root, dirs, files in os.walk(start_root):
        print '{0}: {1:%}'.format(root[len(start_root)+1:], calc_progress(progress, root, dirs))
        

walk('/home')