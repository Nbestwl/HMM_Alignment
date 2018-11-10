# Author: Lei Wang
# Date: 11/09/2018
# EECS 730
# homework 2

import sys
from parser import *
from math import log

# def viterbi(seq, states, start_p, trans_p, emit_p):
#     V = [{}]
#     for st in states:
#         V[0][st] = {"prob": start_p[st] * emit_p[st][seq[0]], "prev": None}
#     # Run Viterbi when t > 0
#     for t in range(1, len(seq)):
#         V.append({})
#         for st in states:
#             max_tr_prob = V[t-1][states[0]]["prob"]*trans_p[states[0]][st]
#             prev_st_selected = states[0]
#             for prev_st in states[1:]:
#                 tr_prob = V[t-1][prev_st]["prob"]*trans_p[prev_st][st]
#                 if tr_prob > max_tr_prob:
#                     max_tr_prob = tr_prob
#                     prev_st_selected = prev_st

#             max_prob = max_tr_prob * emit_p[st][seq[t]]
#             V[t][st] = {"prob": max_prob, "prev": prev_st_selected}

#     for line in dptable(V):
#         print line
#     opt = []
#     # The highest probability
#     max_prob = max(value["prob"] for value in V[-1].values())
#     previous = None
#     # Get most probable state and its backtrack
#     for st, data in V[-1].items():
#         if data["prob"] == max_prob:
#             opt.append(st)
#             previous = st
#             break
#     # Follow the backtrack till the first observation
#     for t in range(len(V) - 2, -1, -1):
#         opt.insert(0, V[t + 1][previous]["prev"])
#         previous = V[t + 1][previous]["prev"]

#     print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob

# def dptable(V):
#     # Print a table of steps from dictionary
#     yield " ".join(("%12d" % i) for i in range(len(V)))
#     for state in V[0]:
#         yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)

def printSeq(state_queue, seq):
    result = []
    for i, state in enumerate(state_queue):
        if state == 'Match':
            result.append(seq[i])
        else:
            result.append('-')

    return result


def viterbi(seq, start_p, trans_p, emit_p, b_f, obs):
    state_queue = []
    positive_match = ['*'] * len(seq)
    v_m = start_p['Match']
    v_i = start_p['Insert']
    v_d = start_p['Delete']

    for i in range(len(seq)):
        xi = seq[i]
        e_m = emit_p[i]['Match'][xi]
        e_i = emit_p[i]['Insert'][xi]
        q_xi = convertProb(float(b_f[obs.index(xi)]))

        first_m = log(e_m / q_xi)
        first_i = log(e_i / q_xi)

        if e_m > q_xi:
            positive_match[i] = '+'

        a_mm = trans_p[i]['Match']['Match']
        a_im = trans_p[i]['Insert']['Match']
        a_dm = trans_p[i]['Delete']['Match']

        a_mi = trans_p[i]['Match']['Insert']
        a_ii = trans_p[i]['Insert']['Insert']

        a_md = trans_p[i]['Match']['Delete']
        a_dd = trans_p[i]['Delete']['Delete']

        prev_v_m = v_m
        prev_v_i = v_i
        prev_v_d = v_d

        if a_mm != 0 and a_im != 0 and a_dm != 0:
            v_m = first_m + max(prev_v_m + log(a_mm), prev_v_i + log(a_im), prev_v_d + log(a_dm))
        else:
            v_m = prev_v_m

        if a_mi != 0 and a_ii != 0:
            v_i = first_i + max(prev_v_m + log(a_mi), prev_v_i + log(a_ii))
        else:
            v_i = prev_v_i

        if a_md != 0 and a_dd != 0:
            v_d = max(prev_v_m + log(a_md), prev_v_d + log(a_dd))
        else:
            v_d = prev_v_d

        maximum = max(v_m, v_i, v_d)
        if v_m == maximum:
            state_queue.append('Match')
        if v_i == maximum:
            state_queue.append('Insert')
        if v_d == maximum:
            state_queue.append('Delete')

    return state_queue, maximum, positive_match

if __name__ == '__main__':
    hmm = sys.argv[1]
    fasta = sys.argv[2]

    match_emissions, insert_emissions, state_transitions, b_f, obs = parser(hmm)
    name, seq = read_fasta(fasta)
    print 'parsing ' + hmm + ' ...'
    print 'file name: ' + name

    seq = list(seq)
    start_p = {'Match': 1.0, 'Insert': 0.0, 'Delete': 0.0}
    trans_p = parse_trans(state_transitions)
    emit_p = parse_emit(match_emissions, insert_emissions, obs)

    state_queue, maximum, positive_match = viterbi(seq, start_p, trans_p, emit_p, b_f, obs)

    print 'maximum score is : ', maximum
    print '\n'
    print 'state list:'
    print state_queue
    print '\n'
    print 'sequence of the profile HMM:'
    print ''.join(printSeq(state_queue, seq))
    print ''.join(positive_match)
