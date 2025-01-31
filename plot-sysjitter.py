#!/usr/bin/env python3
# Plotting routine for the summary.txt file of sysjitter
# https://github.com/alexeiz/sysjitter
#
# Jonathan Coles <jonathan.coles@cscs.ch>
# Updated by: Isa Wazirzada on 31.1.25

import argparse
import pylab as pl
import numpy as np
import pandas as pd
from datetime import datetime

def plot_sysjitter(
        fname_summary,
        fname_freezable,
        fname_image,
        author_name,
        author_email,
        plot_title,
        plot_summary
    ):
    cols = dict()
    with open(fname_summary) as fp:
        for l in fp:
            l = l.split()
            try:
                hdr = l[0].split(':')[0]
                d = list(map(float, l[1:]))
                cols[hdr] = d
            except ValueError:
                pass

    D = pd.DataFrame(cols)

    cores = []
    if fname_freezable:
        try:
            with open(fname_freezable, 'r') as fp:
                for l in fp.readlines():
                    cores += list(map(int, l.split()[1:]))
                print(cores)
        except Exception as e:
            print(f'Warning: {e}. Ignoring freezable.out file')
            pass

    nr = 2
    nc = 2
    fig, axes = pl.subplots(nrows=nr, ncols=nc, figsize=(nc*6, nr*4), squeeze=False)
    pl.subplots_adjust(top=0.75, hspace=0.2)

    pl.suptitle(plot_title)

    author = f'{author_name} <{author_email}>'
    date_time = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

    core_text = ''
    if cores:
        core_text = f'''
                     kworker freezable_power found on cores {cores}.
                     These are marked with magenta vertical lines.
                    '''

    t = f'''
         {plot_summary}
         {core_text}
         Generated on: {date_time}
         Author: {author}
         '''

    header_text = pl.text(0.05, 0.95, t, ha='left', va='top', transform=fig.transFigure, fontsize=9)
    header_text.set_in_layout(False)


    ax = axes[0,0]
    ax.fill_between(D['core_i'], 1e-9 * D['int_max(ns)'],
                                 1e-9 * D['int_min(ns)'], ec='k', fc='k', alpha=0.25)
    ax.plot(D['core_i'], 1e-9 * D['int_median(ns)'], c='g', ls='-', lw=0.5)
    ax.plot(D['core_i'], 1e-9 * D['int_mean(ns)'], c='r', ls='-', lw=0.5)
    ax.plot(D['core_i'], 1e-9 * D['int_total(ns)'], c='b', ls='-', lw=0.5)
    ax.set_xlabel('Core')
    ax.set_ylabel('Time in Interrupts [s]')
    ax.set_yscale('log')
    legend = [
        ['Total',   pl.Line2D([0], [0], lw=5, color='b')],
        ['Mean',    pl.Line2D([0], [0], lw=5, color='r')],
        ['Median',  pl.Line2D([0], [0], lw=5, color='g')],
        ['Min/Max', pl.Line2D([0], [0], lw=5, color='k', alpha=0.25)],
    ]
    for c in cores: ax.axvline(c, lw=0.5, c='m')

    l, h = list(zip(*legend))
    ax.legend(h, l, frameon=False, loc='upper right', ncol=4, fontsize=8, bbox_to_anchor=(1.0, 1.10))

    ax = axes[0,1]
    ax.step(D['core_i'], D['int_total(%)'], c='b', ls='-', lw=0.5, where='mid')
    ax.set_xlabel('Core')
    ax.set_ylabel('% of Runtime in Interrupts')
    ax.set_ylim(ymin=0)
    for c in cores: ax.axvline(c, lw=0.5, c='m')

    ax = axes[1,0]
    ax.step(D['core_i'], D['int_n'], c='b', ls='-', lw=0.5, where='mid')
    ax.set_xlabel('Core')
    ax.set_ylabel('No. Interrupts')
    ax.set_ylim(ymin=0)
    ax.set_yscale('linear')
    for c in cores: ax.axvline(c, lw=0.5, c='m')

    ax = axes[1,1]
    ax.step(D['core_i'], D['int_n_per_sec'], c='b', ls='-', lw=0.5, where='mid')
    ax.set_xlabel('Core')
    ax.set_ylabel('Interrupts / sec')
    ax.set_ylim(ymin=0)
    ax.set_yscale('linear')
    for c in cores: ax.axvline(c, lw=0.5, c='m')

    pl.savefig(fname_image)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot system jitter using the output summary of the sysjitter utility')
    parser.add_argument('--summary_file', type=str, required=True, help='Path to sysjitter summary file')
    parser.add_argument('--freezable_file', type=str, help='Path to freezable.out file')
    parser.add_argument('--image_file', type=str, required=True, help='Path to output image')
    parser.add_argument('--author_name', type=str, required=True, help='Name of the author')
    parser.add_argument('--author_email', type=str, required=True, help='Email of the author')
    parser.add_argument('--plot_title', type=str, default='System jitter', help='Title of the plot')
    parser.add_argument('--plot_summary', type=str, default='System jitter as recorded on a node using ./sysjitter --runtime 300 --verbose 300', help='Summary string of the plot')

    args = parser.parse_args()

    plot_sysjitter(
        args.summary_file,
        args.freezable_file,
        args.image_file,
        args.author_name,
        args.author_email,
        args.plot_title,
        args.plot_summary
    )
