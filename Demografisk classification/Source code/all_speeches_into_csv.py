import os
import textstat as tx
import spacy

# declare what has to be
path_for_data = "/home/gregkoncz/git/FYP_miniprojekt3/data/TranscriptsOfPresidents"
path_for_targets = "/home/gregkoncz/git/FYP_miniprojekt3/data/presidents_info.csv"
substrings_to_look_for = [".", "!", "?", ",", " ", " I ", " we ", "America", "war", "terrorism", "a", "b", "c", "d", "e", "ed", " will ", "russia", "bomb", "great", "family", "happy", "child", "peace", "enemy", "soldier", "excuse"]
word_types = ["VERB", "ADJ", "PROPN"]

# function to get target variables
def return_target_variables():
    target_dicts = {}
    with open(path_for_targets, "r") as this_file:
        header = this_file.readline()
        for line in this_file:
            target_dicts[line.strip().split(",")[0]] = line.strip().split(',')[1:]
    return target_dicts

# func to build list of all speeches
def metrics_for_all_files():
    speech_counter = 0
    list_of_measures_per_speech = []
    folders = [folder for folder in os.listdir(path_for_data) if "complete" not in folder]

    for folder in folders:
        new_path = path_for_data + "/" + folder
        files = [file for file in os.listdir(new_path) if ("all" not in file and ".txt" in file)]

        for file in files:
            current_list = [folder]
            current_file_path = new_path + "/" + file

            with open(current_file_path, "r") as this_file:
                all_text = " ".join(this_file.readlines())
                if len(all_text) < 10:
                    continue
                for subs in substrings_to_look_for:
                    current_list.append(all_text.upper().count(subs.upper()))
                current_list.append(len(all_text))
                current_list.append(sum(current_list[1:4]))
                flesh_score = tx.flesch_reading_ease(all_text)
                if flesh_score > 0:
                    current_list.append(flesh_score)
                else:
                    current_list.append(0)
                current_list.append(tx.smog_index(all_text))

                # some speeches were too long

                if len(all_text) < 1000000:
                    doc = nlp(all_text)
                    verb_c = 0
                    adj_c = 0
                    pronoun_c = 0
                    for token in doc:
                        if token.pos_ == "VERB":
                            verb_c += 1
                        elif token.pos_ == "ADJ":
                            adj_c += 1
                        elif token.pos_ == "PROPN":
                            pronoun_c += 1
                    current_list.append(verb_c)
                    current_list.append(adj_c)
                    current_list.append(pronoun_c)
                else:
                    for i in range(3):
                        current_list.append("")

                for i in range(len(current_list)):
                    current_list[i] = str(current_list[i])
                list_of_measures_per_speech.append(current_list)
                speech_counter += 1
                print(speech_counter)

    return list_of_measures_per_speech

# function to unionize the two data structure
def unionize_data_structures(metrics_list, target_dictionary):
    for line in metrics_list:
        for target in target_dictionary[line[0]]:
            line.append(str(target))
    return metrics_list

# function write dictionary into csv
def write_dict_to_csv(list_to_write):
    this_file =  open("/home/gregkoncz/git/FYP_miniprojekt3/data/all_speech_data/all_speeches_measures.csv", "w")
    this_file.write("name,dots,exclmark,questionmark,commas,spaces,Is,wes,America,war,terrorism,a,b,c,d,e,ed,will,russia,bomb,great,family,happy,child,peace,enemy,soldier,excuse,letters,punctuation,flesch_read,smog_read,verb_count,adjektiv_count,pronoun_count,state,democrat,age_by_election,married,has_children,cheater,higher_edu,war_time,historical_period,assassinated,elected\n")
    for line in list_to_write:
        this_file.write(",".join(line) + "\n")

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    all_measures_list = metrics_for_all_files()
    target_dicts = return_target_variables()
    final_list = unionize_data_structures(all_measures_list, target_dicts)
    print(final_list)
    write_dict_to_csv(final_list)
