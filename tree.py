#!/usr/bin/python

# tree.py -- "gnu" -like tree utility

import sys

HELP = '''\
tree -- "gnu" -like tree utility

usage:

    $ tree < tree.txt
    $ tree 
    $ tree diff a.txt < b.txt
    $ tree prune id ...
'''

def output(s):
    sys.stdout.write(s.encode('utf-8'))


def load(f):
    root = [0, None, None, []]      # depth, parent, text, children
    parent = root
    for i in f.readlines():
        i = i[:-1].decode('utf-8')
        t = 0
        for j in i:
            if j in (' ','\t'):
                t += 1
            else:
                break
        if 0 == t:
            parent = root
        elif t == parent[3][-1][0]:
            pass
        elif t > parent[3][-1][0]:
            parent = parent[3][-1]
        elif t < parent[3][-1][0]:
            while 1:
                parent = parent[1]
                if parent[0] < t:
                    break
        node = [t, parent, i[t:], []]
        parent[3].append(node)
    return root


def dump_helper(root, depth, indent):
    output(' ' * (depth * indent))
    output(root[2])
    output('\n')
    for i in root[3]:
        dump_helper(i, depth + 1, indent)


def dump(root, indent = 4):
    dump_helper(root, 0, indent)
    

def dump_roots(root, indent = 4):
    for i in root[3]:
        dump_helper(i, 0, indent)


def find(root, prefix):
    if None != root[2] and root[2].startswith(prefix):
        return root
    for i in root[3]:
        x = find(i, prefix)
        if None != x:
            return x
    return None


def main(argv):
    if 0 == len(argv):
        print(HELP)
        sys.exit(0)

    c = argv[0]
    if 0:
        pass
 
    elif 'cat' == c:
        root = load(sys.stdin)
        dump_roots(root)

    elif 'clip' == c:
        root = load(sys.stdin)
        n = find(root, argv[1])
        if None != n:
            dump(n)

    elif 'prune' == c:
        root = load(sys.stdin)
        n = find(root, argv[1])
        if None != n:
            parent = n[1]
            for i in n[3]:
                i[1] = parent
                parent[3].append([n[0], parent, i[2], i[3]])
            for idx, i in enumerate(parent[3]):
                if i == n:
                    parent[3] = parent[3][:idx] + parent[3][idx + 1:]
        dump_roots(root)

    elif 'add' == c:
        root = load(sys.stdin)
        n = find(root, argv[1])
        if None != n:
            if 0 == len(n[3]):
                n[3].append([n[0] + 4, n, argv[2], []])
            else:
                n[3].append([n[3][0][0], n, argv[2], []])
            dump_roots(root)

    else:
        print('i don\'t know how to "%s".' % c)
        print(HELP)
        sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])
