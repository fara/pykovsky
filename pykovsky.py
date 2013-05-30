from PMIDI.Composer import Sequencer
import time
import random

C_SCALE = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

CHORDS = {'C': ['C', 'E', 'G'], 
          'D': ['D', 'F', 'A'],
          'd': ['D', 'F', 'A'],
          'E': ['E', 'G', 'B'],
          'F': ['F', 'A', 'C'],          
          'G': ['G', 'B', 'D'],
          'A': ['A', 'C', 'E'],
          'a': ['A', 'C', 'E'],
          'B': ['B', 'D', 'F']}

F_PROG = [[5, 5, 5, 4, 4, 4, 6, 6, 1, 3], 
          [5, 5, 5, 4, 4, 6, 6, 1, 3],
          [6, 6, 6, 4, 4, 1, 2, 5],
          [5, 5, 5, 1, 1, 2, 2, 3, 6],
          [1, 1, 1, 4, 4, 6, 6, 2, 3],
          [2, 2, 2, 5, 5, 3, 3, 4, 4, 1],
          [1, 1, 1, 3, 3, 3, 6, 6, 2, 4]]

def get_next_chord(chord):
    """ Gets a chord to add to the progression based on the fundamental progression rules """
    
    num = C_SCALE.index(chord)
    candidates = F_PROG[num-1]
    return C_SCALE[random.choice(candidates)]
    
def add_chord(meas, chord_name):
    """ Adds a chord to the measure """
    
    for note in CHORDS[chord_name]:
        meas.NewNote(0, 64, note, 5)

def create_base(inst):
    """ Creates the chord progression """

    strophe = []
    chorus = []
    chord = C_SCALE[0]
    
    for i in range(4):
        strophe.append(chord)        
        chord = get_next_chord(chord)
    
    for i in range(4):
        chorus.append(chord)        
        chord = get_next_chord(chord)
    
    chord_progression = strophe + strophe + chorus + strophe
        
    for c in chord_progression:
        meas = inst.NewMeasure()
        add_chord(meas, c)

    return chord_progression
        
    
def get_rdm_note(chord, last_note):
    """ Gets a random note based on the current chord """
    
    if random.randint(1,10) <= 6:
        # chord note
        return random.choice(CHORDS[chord])   
    else:
        # scale note    
        n = C_SCALE.index(last_note)
        return C_SCALE[n+random.choice(range(-n, 6-n)[2:5])]
    
def create_melody(inst, chord_progression):
    """ Creates the melody for the chord progression """
    
    for chord in chord_progression:
        
        meas = inst.NewMeasure()
        last_note = random.choice(CHORDS[chord])
        pos = 0
        
        while pos < 64:
            dur = random.choice([8, 8, 16, 16])            
            last_note = get_rdm_note(chord, last_note)
            if random.randint(1,10) <= 8: # 20% silence
                meas.NewNote(pos, dur, last_note, 5)
            pos += dur
            

# create the sequencer
seq = Sequencer()
# create a new song
song = seq.NewSong()

# add an instrument to the song
b_inst = song.NewVoice()
cp = create_base(b_inst)
print cp

bajo = song.NewVoice()
for c in cp:
    meas = bajo.NewMeasure()
    meas.NewNote(0, 32, c, 3)
    meas.NewNote(32, 32, c, 3)
                       
m_inst = song.NewVoice()
create_melody(m_inst, cp)

# play the song
seq.Play()

# wait; the song plays asynchronously
time.sleep(30)
