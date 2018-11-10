# Author: Lei Wang
# Date: 11/09/2018
# EECS 730
# homework 2

from math import exp

def parser(filename):
	index = 0
	table, match_emissions, insert_emissions, state_transitions, avg = [], [], [], [], []

	with open(filename) as fp:
		l = [line for line in fp]
		for i, line in enumerate(l):
			if line.startswith('HMM '):
				index = i

		for line in l[index:]:
			table. append(line)

	obs = table[0].split()[1:]
	transitions = table[1].split()

	table = table[2:]
	for x in table[0:3]:
 		avg.append(x.split())
 	table = table[3:-1]

 	for x in range(len(table)/3):
 		match_emissions.append(table[x*3].split()[1:len(avg[1])+1])
 		insert_emissions.append(table[x*3+1].split())
 		state_transitions.append(table[x*3+2].split())

 	return match_emissions, insert_emissions, state_transitions, avg, obs


def convertProb(num):
    return exp(-float(num)) if num != '*' else 0


def parse_trans(transitions):
	trans_p = []

	for transition in transitions:
		trans, match, insert, delete = {}, {}, {}, {}
        match = {
            'Match': convertProb(transition[0]),
            'Insert': convertProb(transition[1]),
            'Delete': convertProb(transition[2]),
        }

        insert = {
            'Match': convertProb(transition[3]),
            'Insert': convertProb(transition[4]),
        }

        delete = {
            'Match': convertProb(transition[5]),
            'Delete': convertProb(transition[6]),
        }

        trans = {
            'Match': match,
            'Insert': insert,
            'Delete': delete
        }

        trans_p.append(trans)

	return trans_p


def parse_emit(match_emissions, insert_emissions, obs):
	emit_p = []

	for emission in range(len(match_emissions)):
		emits, match, insert = {}, {}, {}

		for i in range(len(obs)):
			match[obs[i]] = convertProb(match_emissions[emission][i])
			insert[obs[i]] = convertProb(insert_emissions[emission][i])

		emits = {
			'Match': match,
			'Insert': insert
		}

		emit_p.append(emits)

	return emit_p

