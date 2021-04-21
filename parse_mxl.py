import music21 as m21
import os
from tqdm import tqdm


def display_file(filepath):
    path_dir = os.listdir(filepath)
    print(path_dir)


def output_lyrics(filepath):
    path_list = os.listdir(filepath)
    for filename in tqdm(path_list):
        try:
            data = m21.converter.parse(filepath + '/' + filename)
            all_text = m21.text.assembleLyrics(data.parts[0])
            # print(all_text)
            with open(filepath + "/lyrics/" + filename[:-4] + ".txt", 'w', encoding='utf-8') as file:
                file.write(all_text)
        except BaseException:
            print("ERROR:" + filename)
            continue


def display_info(data):
    # print(len(data.parts))
    for i in range(len(data.parts)):
        part = data.parts[i].flat
        print(len(part.notesAndRests))
        for k in range(len(part.notesAndRests)):
            event = part.notesAndRests[k]
            if isinstance(event, m21.note.Note):
                note_name = event.name
                note_octave = event.octave
                note_duration = event.duration.quarterLength
                note_beat = event.beat - 1
                note_beat_strength = event.beatStrength
                token = event.lyrics[0].text if len(
                    event.lyrics) > 0 else "<NULL>"
                print(
                    str(note_name) +
                    str(note_octave),
                    note_beat,
                    note_beat_strength,
                    note_duration,
                    token)
            elif isinstance(event, m21.note.Rest):
                frequency = 0
                token = "<NULL>"
                print(frequency, token)


if __name__ == '__main__':
    path = "D:/Dataset02_Wikifonia"
    #path = "D:/Dataset01_CPDL"
    # display_file(path)
    # output_lyrics(path)
    data = m21.converter.parse(
        "D:\\Dataset02_Wikifonia\\Michael Jackson - Beat it!.mxl")
    # display_info(data)
    data.parts[0].plot()
    # segments = m21.analysis.segmentByRests.Segmenter.getSegmentsList(data)
    # print(segments)
    # print(m21.search.segment.indexOnePath("D:\\Dataset01_CPDL\\1914 (James Crawford).mxl"))
