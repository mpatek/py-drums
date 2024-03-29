import itertools
import random


def bit_voices_to_notes(bit_voices, note_value=4):
    """ Multiple voices combined as one. """
    notes = []
    # we assume all bit strings have same length.
    n_notes = len(bit_voices.values()[0])
    for i in range(n_notes):
        note = None
        notes_i = [k for k in bit_voices if bit_voices[k][i] == '1']
        if not notes_i:
            note = 'r'
        elif len(notes_i) == 1:
            note = notes_i[0]
        else:
            note = '<{0}>'.format(' '.join(notes_i))
        if not notes:
            note = note + str(note_value)
        notes.append(note)
    return notes


def bits_to_notes(bits, voice="sn", note_value=4):
    """ Returns a list of notes or rests or voice based on bits in bit string. """
    notes = []
    for bit in bits:
        note = None
        if bit == '0':
            note = 'r'
        else:
            note = voice
        if not notes:
            note = note + str(note_value)
        notes.append(note)
    return notes


def drum_voice(varname, notes):
    """ Returns a string representation of a drum voice. """
    return '{0} = \\repeat volta 2 \drummode {{ {1} }}'.format(varname, ' '.join(notes))


def drum_staff(voices, directives):
    """ Returns string representation of a drum staff. """
    parts = ['\\new DrumStaff <<']
    for directive in directives:
        parts.append('  ' + directive)
    for voice, varname in voices.items():
        parts.append('  \\new DrumVoice { \\voice'+voice+' \\'+varname+' }')
    parts.append('>>')
    return "\n".join(parts)


def int_to_binstr(x, n_notes):
    return str(bin(x)).replace('0b', '').zfill(n_notes)


def drum_permutation_generator(
        combinations,
        instruments,
        n_notes=4,
        note_value=4,
        ):
                
    n_instr = len(instruments)
    voices = {
            'One': {'instruments': range(0, n_instr/2), 'varname': 'up'},
            'Two': {'instruments': range(n_instr/2, n_instr), 'varname': 'down'},
            }
    for i, comb in enumerate(combinations):
        lines = []
        for voice in voices:
            instr_bs = {}
            for instr_idx in voices[voice]['instruments']:
                instr = instruments[instr_idx]
                instr_bs[instr] = int_to_binstr(comb[instr_idx], n_notes)
            notes = bit_voices_to_notes(instr_bs, note_value)
            lines.append(drum_voice(voices[voice]['varname'], notes))
        lines.append(drum_staff(
            dict((v, k['varname']) for v, k in voices.items()),
            ['\\mark "{0}."'.format(i + 1)],
            ))
        yield lines


def permutation_combinations(n_notes, n_instr, n_combinations=100, maxn_zeros=1):
    n_seen = 0
    for comb in itertools.combinations_with_replacement(
            range(2 ** n_notes), n_instr,
            ):
        n_zeros = sum(1 for x in comb if x == 0)
        if n_zeros > maxn_zeros:
            continue
        yield comb
        n_seen += 1
        if n_seen >= n_combinations:
            break

def random_combinations(n_notes, n_instr, n_combinations=100, maxn_zeros=1):
    for i in range(n_combinations):
        comb = [random.randint(0, 2 ** n_notes - 1) for x in range(n_instr)]
        n_zeros = sum(1 for x in comb if x == 0)
        if n_zeros > maxn_zeros:
            continue
        yield comb


"""
instruments = ['hh', 'sn', 'bd', 'hhp']
for x in drum_permutation_generator(instruments, n_notes=16, note_value=16):
    print "\n".join(x)
"""
instruments = ['hh', 'sn', 'bd', 'hhp']
#combs = permutation_combinations(4, len(instruments), maxn_zeros=0)
combs = random_combinations(4, len(instruments))
for x in drum_permutation_generator(combs, instruments, n_notes=4, note_value=4):
    print "\n".join(x)
