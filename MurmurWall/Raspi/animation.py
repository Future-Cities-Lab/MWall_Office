#!/usr/bin/python

from itertools import repeat
from Queue import Queue
from time import time, sleep
from random import uniform, shuffle, randint


from Packet import Packet
from LedMatrix import LedMatrix

from port_manager import get_matrix_port
from data_manager import get_latest_data, get_whispers, get_curated_words

from RepeatedTimer import RepeatedTimer

CURATED_LENGTH = 60
NEW_WORD_LENGTH = 3

def update_queue():
    related_terms_queue = Queue()
    trend_buckets = get_latest_data()
    related_terms_list = []
    for trend in trend_buckets:
        for related_term in trend_buckets[trend]["Top searches for"]:
            term = related_term.upper().encode('ascii', 'ignore')
            if term not in related_terms_list:
                related_terms_list.append(term)
    shuffle(related_terms_list)
    for i in range(0, len(related_terms_list)):
        related_terms_queue.put(related_terms_list[i])
    print '\nRelated_Terms size = %i\n' % (related_terms_queue.qsize(),)
    return related_terms_queue

def check_whispers(whispers_queue):
    new_whispers = get_whispers()
    if len(new_whispers) > 0:
        for whisper in new_whispers:
            if not whisper == '' and not whisper == "":
                whispers_queue.put(whisper)


def main():
    try:
        matrix = LedMatrix(get_matrix_port())

        trending_words_queue = update_queue()
        
        whispers_queue = Queue()
        rt = RepeatedTimer(5, check_whispers, whispers_queue)
    
        curated_words = get_curated_words()

        packets = Queue()
        for _ in repeat(None, trending_words_queue.qsize()):
            text = trending_words_queue.get()
            color = (chr(255), chr(randint(0, 255)), chr(255))
            new_packet = Packet(40, color, text)
            packets.put(new_packet)
                    
        prev_curated_time = time()
        curated_pos = 0

        prev_new_word_time = time()

        while True:
            if not whispers_queue.empty():
                whisper = Packet(40, (chr(0), chr(255), chr(255)), whispers_queue.get())
                matrix.update_hardware(whisper)            
            if time() -  prev_curated_time >= CURATED_LENGTH:
                prev_curated_time = time()
                curated_packet = Packet(40, (chr(255), chr(255), chr(255)), curated_words[curated_pos])
                matrix.update_hardware(curated_packet)
                curated_pos += 1
                curated_pos %= len(curated_words)
            if time() - prev_new_word_time >= NEW_WORD_LENGTH:
                prev_new_word_time = time()
                packet = packets.get()
                matrix.update_hardware(packet)
                packets.put(packet)
            sleep(0.10)

    except IOError:
        print '\nIOError, Shutting down  MurmurWall\n'
            
    
if __name__ == "__main__":
    print '\nStarting MurmurWall (Office Edition!)\n'
    main()
