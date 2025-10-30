import gzip
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('fqfile', help='FASTQ gzip file to analyze')
    parser.add_argument('-t', type=str, required=True, help='File containing tags, one per line')
    parser.add_argument('-s', type=int, default=0, help='Start nucleotide to search for tags')
    args = parser.parse_args()
    return args

def starts_with_any(txt, match_list, beg=0):
    for el in match_list:
        if txt.startswith(el, beg):
            return True
    return False

def read_tags(tagfile):
    tags = list()
    with open(tagfile, 'r') as infile:
        for l in infile:
            tags.append(l.strip())
    return tags

def do_count(fqfile, tags, beg):
    matched = 0
    unmatched = 0
    with gzip.open(fqfile, 'rt') as infile:
        for l in infile: # loop through every line
            if l.strip().startswith('@'): # each 4-line read starts with an @ identifier line
                read = infile.readline().strip() # grab the read - line 2
                if starts_with_any(read, tags, beg): # does it start with the tag
                    matched += 1
                else: # or not
                    unmatched += 1
    tot = matched + unmatched
    match_perc = (matched / tot) * 100
    unmatch_perc = (unmatched / tot) * 100
    print('***********************')
    print(fqfile)
    print('***********************')
    print('Total reads: {0}'.format(tot))
    print('-----------------------')
    print('Tag Match: {0} ({1:.1f}%)'.format(matched, match_perc))
    print('No Match:  {0} ({1:.1f}%)'.format(unmatched, unmatch_perc))
    print('***********************')

def main():
    args = parse_args()
    fqfile = args.fqfile
    tags = read_tags(args.t)
    beg = args.s
    do_count(fqfile, tags, beg)

if __name__ == '__main__':
    main()
