import framework.feedMaker.dataCreator as dc

songPath = 'dump/test_mapset/audio.mp3'
beatmapPath = 'dump/test_mapset/Kurahashi Yoeko - Tomodachi no Uta (tutuhaha) [Light Insane].osu'
interval = 25

data_spliced, data_fresh = dc.create_dataset(songPath,beatmapPath,interval,1)

print('Is the each of the spliced data paired to others?\n\t{0}\n'.format(len(data_spliced[0])==len(data_spliced[1])))

print('The shape of one data for one iteration:')
print('Input data : {0}{1}'.format(data_spliced[0][0].shape,' ; needs reshaping' if len(data_spliced[0][0].shape)!=2 else ''))
print('Label data : {0}{1}'.format(data_spliced[1][0].shape,' ; needs reshaping' if len(data_spliced[1][0].shape)!=2 else ''))