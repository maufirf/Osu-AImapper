import framework.objectSync as os
import io_custom.mapRead as mr
from time import sleep

timeline = os.timeliner_std(mr.readObjects("dump/fhana - Sorairo Picture (Sotarks) [Haruto's Insane].osu",returnAsBeatmap=True))
nutimeline = os.timelineSplicer(timeline,50)
input("press enter to start")
for ms in nutimeline:
    if ms[0]:print('[[CIRCLE]]')
    elif ms[1]:print('[[SLIDER]]')
    elif ms[2]:print('[[SPINNER]]')
    else:print('...')
    sleep(0.05)