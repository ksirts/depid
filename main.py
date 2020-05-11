description = """
Compute PID score by counting dependency types.
"""

# Usage:    python deppid.py <text file>
# or        python deppid.py < <text file>
# Outputs:  If the file is read from standard input then just prints the
#           PID score. If the file is given as a command line argument
#           then attempts to extract data from the file name and prints
#           if with the PID feature as a tab-separated data

#   Copyright 2019 Kairit Sirts
#   kairit.sirts@gmail.com

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import argparse
import os
import glob
import sys

import spacy

from depid.utils import safe_division
from depid.pid import Depid

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-F', '--folder', help='Input folder containing text files')
    parser.add_argument('-f', '--file', help='Single input file')
    parser.add_argument('-O', '--output', help="""Write propositions report files into this folder. 
                        If not given then creates a new 'output' folder in the current working directory""")
    parser.add_argument('-C', '--conj', action='store_true',
                        help="""
                        Count also conjunctions as propositions. This has the side effect of counting 
                        as propositions the sentence-initial conjunction words that serve as lexical fillers. 
                        """)
    args = parser.parse_args()

    if args.folder is not None:
        if not os.path.isdir(args.folder):
            raise ValueError(f"The input folder '{args.folder}' does not exist")
        filenames = glob.glob(os.path.join(args.folder, '*.txt'))
    else:
        if args.file is None:
            raise ValueError("Either -F <folder> or -f <file> must be given")
        if not os.path.exists(args.file):
            raise ValueError(f"File '{args.file}' does not exist")
        filenames = [args.file]

    if args.output is not None:
        output_path = args.output
        if not os.path.isdir(output_path):
            print(f"The output folder '{output_path}' does not exist", file=sys.stderr)
            os.mkdir(output_path)
            print(f"Output folder '{output_path}' created", file=sys.stderr)
    else:
        cwd = os.getcwd()
        output_path = os.path.join(cwd, 'depid_output')
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
            print(f"Output folder '{output_path}' created", file=sys.stderr)


    nlp = spacy.load('en_core_web_sm', disable=["ner"])
    print('filename\tprop1\tprop_rep\twords\tdepid\tdepid_rep')

    for fn in filenames:
        basename = os.path.basename(fn)
        file_stem, _ = os.path.splitext(basename)
        outfile = os.path.join(output_path, file_stem + '.prop')

        prop_counter = Depid(count_conjunctions=args.conj)

        with open(fn) as f_in, open(outfile, 'w') as f_out:
            for line in f_in:
                txt = nlp(line.strip())
                for sent in txt.sents:
                    tokens_out = prop_counter.count_propositions(sent)
                    for i, (word, lemma, pos, head, dep, tok, prop, rep) in enumerate(tokens_out):
                        print(f'{i+1}\t{word}\t{lemma}\t{pos}\t{head}\t{dep}\t{tok}\t{prop}\t{rep}', file=f_out)
                    print(file=f_out)
        num_props = prop_counter.num_propositions()
        num_props_rep = prop_counter.num_propositions(rep=True)
        num_tokens = prop_counter.num_tokens
        prop_id = safe_division(num_props, num_tokens)
        prop_rep_id = safe_division(num_props_rep, num_tokens)
        print(f'{basename}\t{num_props}\t{num_props_rep}\t{num_tokens}\t{prop_id:.3f}\t{prop_rep_id:.3f}')