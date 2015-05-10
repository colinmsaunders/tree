#!/usr/bin/python

# tree.py -- "gnu" -like tree utility

import sys

HELP = '''\
tree.py -- "gnu" -like tree utility

a tree is a line based text file, indents indicate parent-child relationship

usage:

    $ cat tree.txt | python tree.py [command] > tree2.txt

commands:

    help            -- show this help
    cat             -- just parse input and write to stdout
    clip <s>        -- "clip" first sub-tree that starts with <s>
    prune <s>       -- "prune" first sub-tree that starts with <s>
    find <s>        -- find node that starts with <s>
    add <s> <n>     -- add new node under <s>
    move <a> <b>    -- move subtree at <a> under <b>
    sort            -- sort children
    count           -- dump tree with counts
'''

INDENT = 4


def output(s):
    sys.stdout.write(s.encode('utf-8'))


def load(f):
    root = [0, None, None, []]      # indent, parent, text, children
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


def count_under(root):
    t = 1
    h = 0
    for i in root[3]:
        a,b = count_under(i)
        t += a
        h = max(h, b)
    return (t, h + 1)


def dump_helper(root, depth, counts):
    if counts:
        # HACK: gross n^n algo
        under, height = count_under(root)
        output('%d\t%d\t%d\t%d\t' % (depth, height, len(root[3]), under))
    output(' ' * (depth * INDENT))
    output(root[2])
    output('\n')
    for i in root[3]:
        dump_helper(i, depth + 1, counts)


def dump(root, counts = False):
    dump_helper(root, 0, counts)
    

def dump_roots(root, counts = False):
    for i in root[3]:
        dump_helper(i, 0, counts)


def find(root, prefix):
    if None != root[2] and root[2].startswith(prefix):
        return root
    for i in root[3]:
        x = find(i, prefix)
        if None != x:
            return x
    return None


def sort_children(root):
    root[3].sort()
    for i in root[3]:
        sort_children(i)


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

    elif 'find' == c:
        root = load(sys.stdin)
        n = find(root, argv[1])
        if None != n:
            output('%s\n' % n[2])

    elif 'add' == c:
        root = load(sys.stdin)
        n = find(root, argv[1])
        if None != n:
            if 0 == len(n[3]):
                n[3].append([n[0] + 4, n, argv[2], []])
            else:
                n[3].append([n[3][0][0], n, argv[2], []])
            dump_roots(root)

    elif 'move' == c:
        root = load(sys.stdin)
        n1 = find(root, argv[1])
        if 0 == len(argv[2]):
            n2 = root
        else:
            n2 = find(root, argv[2])
        if None != n1 and None != n2:
            if 0 == len(n2[3]):
                n2[3].append([n2[0] + 4, n2, n1[2], n1[3]])
            else:
                n2[3].append([n2[3][0][0], n2, n1[2], n1[3]])
            dump_roots(root)
 
    elif 'sort' == c:
        root = load(sys.stdin)
        sort_children(root)
        dump_roots(root)
     
    elif 'count' == c:
        root = load(sys.stdin)
        dump_roots(root, True)

    else:
        print('i don\'t know how to "%s".' % c)
        print(HELP)
        sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])
