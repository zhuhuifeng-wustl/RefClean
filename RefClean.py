import os
import re
from collections import defaultdict
import numpy as np
import time


def main(bib_path="./bib", rpt_path="./", rpt_name="RefClean_Report.txt", mode=0):
    # bib_path = "./bib"
    # rpt_path = "./"
    # rpt_name = "RefClean_Report.txt"

    print_line()
    print("RefClean: An automatic tool for duplicated references checking.")
    print("Washington University in St.Louis - Huifeng Zhu (zhuhuifeng@wustl.edu)\n")
    time_stamp = time.strftime('%m/%d/%Y-%H:%M:%S', time.localtime(time.time()))
    print(time_stamp)

    # read all the files in the directory
    files = os.listdir(bib_path)

    # scan bib files
    files_bib = []
    for file in files:
        if ".bib" in file:
            files_bib.append(file)
    files_bib_num = len(files_bib)
    print_line()
    print("Scanning for the bib files in %s." % bib_path)
    print("Detected %d bib files:" % files_bib_num)
    for file in files_bib:
        print("\t", file)

    # read the bib references
    print("Reading the bib references...")
    reference = [["file name", "start line number", "end line number", "type", "cite name", "title", "raw_bib"]]
    reference_titles = []
    reference_cites = []
    str_tmp = ""
    cite_name = ""
    type_name = ""
    for file in files_bib:
        f = open(bib_path + "/" + file, 'r')
        iter_f = iter(f)
        line_num = 0
        left_brace_num = 0
        right_brace_num = 0
        start_num = 0
        for line in iter_f:
            line_num += 1
            line = line.replace('\n', '')
            if '%' in line and '\\%' not in line:
                pass
            else:
                if "@" in line and left_brace_num == 0:
                    start_num = line_num
                    left_brace_num = line.count('{')
                    right_brace_num = line.count('}')
                    str_tmp = str_tmp + line
                    # read type name
                    search_obj = re.search(r'@(.*?){', line, re.S)
                    if search_obj is None:
                        exit("Wrong bib reference when extract type name: %s:%d\n line:%s" % (
                            bib_path + "/" + file, start_num, line))
                    else:
                        type_name = search_obj.group(1)
                    # read cite name
                    search_obj = re.search(r'{(.*?),', line, re.S)
                    if search_obj is None:
                        cite_name = "None"
                        # print("Wrong bib reference when extract cite name: %s:%d\n line:%s" % (
                        # bib_path + "/" + file, start_num, line))
                    else:
                        cite_name = search_obj.group(1)
                        # print(cite_name)
                else:
                    left_brace_num = left_brace_num + line.count('{')
                    right_brace_num = right_brace_num + line.count('}')
                    str_tmp = str_tmp + line
                if left_brace_num == right_brace_num and left_brace_num != 0:
                    end_num = line_num
                    str_tmp = str_tmp.replace(' ', '')
                    str_tmp = str_tmp.replace('\t', '')
                    # read title
                    search_obj = re.search(r',title={(.*?)}[,}]', str_tmp, re.S | re.I)
                    if search_obj is None:
                        # print("Wrong bib reference when extract title: %s:%d-%d\n line:%s" % (
                        # bib_path + "/" + file, start_num,end_num, str_tmp))
                        title = "None"
                    else:
                        title = search_obj.group(1)
                        # print(title)
                    reference.append([bib_path + "/" + file, start_num, end_num, type_name, cite_name, str_tmp])
                    reference_titles.append("".join(list(filter(str.isalnum, title.lower()))))
                    reference_cites.append(cite_name)
                    str_tmp = ""
                    left_brace_num = 0
                    right_brace_num = 0
    print("Imported %d bib references." % (len(reference) - 1))
    print_line()
    # process the reference library
    print("Start extracting the information from bib library...")
    print("Checking the duplicated items...")
    reference_duplicated = []

    for dup in sorted(list_duplicates(reference_titles)):
        reference_duplicated.append(dup)
        # print(dup)
    reference_none_num = 0
    reference_duplicated_num = 0
    for dup in reference_duplicated:
        if dup[0] != "none":
            reference_duplicated_num = reference_duplicated_num + len(dup[-1])
        else:
            reference_none_num = reference_none_num + len(dup[-1])
    print("Detected %d duplicated references (includes %d items)." % (
        len(reference_duplicated), reference_duplicated_num))
    # check the entries of duplicated references
    reference_duplicated_diff_cites = []
    reference_duplicated_diff_cites_num = 0
    print("Checking the entries of the duplicated items...")
    for dup in reference_duplicated:
        if dup[0] != "none":
            cites = []
            for ind in dup[-1]:
                cites.append(reference_cites[ind])
            if_cites_same = 1
            for i in range(len(cites)):
                for j_cite in cites[i + 1:]:
                    if cites[i] != j_cite:
                        if_cites_same = 0
                        break
                if if_cites_same == 0:
                    break
            if if_cites_same is 0:
                reference_duplicated_diff_cites.append(dup)
                reference_duplicated_diff_cites_num = reference_duplicated_diff_cites_num + len(dup[-1])
    print("Detected %d of all duplicated references have different entries (includes %d items)." % (
        len(reference_duplicated_diff_cites), reference_duplicated_diff_cites_num))

    # write report
    print_line()
    print("Generating report...")
    rpt = open(rpt_path + '/' + rpt_name, "w")
    rpt.write("-------------------------------------\n")
    rpt.write("RefClean: An Automatically tool for duplicated references checking.\n")
    rpt.write("Washington University in St.Louis - Huifeng Zhu (zhuhuifeng@wustl.edu)\n")
    rpt.write(time_stamp + "\n")
    rpt.write("-------------------------------------\n")
    rpt.write("Scanning for the bib files in %s.\n" % bib_path)
    rpt.write("Detected %d bib files:\n" % files_bib_num)
    for file in files_bib:
        rpt.write("\t" + file + '\n')
    rpt.write("-------------------------------------\n")
    rpt.write("Imported %d bib references.\n" % (len(reference) - 1))
    rpt.write("Detected %d duplicated references (includes %d items).\n" % (
        len(reference_duplicated) - 1, reference_duplicated_num))
    rpt.write("Detected %d of all duplicated references have different entries (includes %d items).\n" % (
        len(reference_duplicated_diff_cites), reference_duplicated_diff_cites_num))
    rpt.write("\n")
    rpt.write("\n")
    rpt.write("======================== Report ========================\n")
    rpt.write("\n")
    rpt.write("================================================\n")
    rpt.write("The duplicated items with different entries:\n")
    print_dup(reference_duplicated_diff_cites, reference, rpt)
    rpt.write("================================================\n")
    rpt.write("All duplicated items:\n")
    print_dup(reference_duplicated, reference, rpt)

    rpt.write("================================================\n")
    rpt.write("The items that need further check:\n")
    for i in range(len(reference_titles)):
        # print(i)
        if re.match(reference_titles[i], 'none', re.I):
            rpt.write("\n")
            ref = reference[i + 1]
            rpt.write("In %s : %d-%d :\n" % (ref[0], int(ref[1]), int(ref[2])))
            with open(ref[0], 'r') as x:
                line = x.readlines()
                for j in range(int(ref[1]) - 1, int(ref[2])):
                    rpt.write('\t' + line[j])
                # rpt.writelines(line[ref[1]-1:ref[2]])
                rpt.write("\n")

    for i in range(len(reference_cites)):
        if re.match(reference_cites[i], 'none', re.I):
            rpt.write("\n")
            ref = reference[i + 1]
            rpt.write("In %s : %d-%d :\n" % (ref[0], int(ref[1]), int(ref[2])))
            with open(ref[0], 'r') as x:
                line = x.readlines()
                for j in range(int(ref[1]) - 1, int(ref[2])):
                    rpt.write('\t' + line[j])
                # rpt.writelines(line[ref[1]-1:ref[2]])
                rpt.write("\n")
            # print(reference[i])
    print("Report written in %s" % rpt_path + '/' + rpt_name)


def print_line():
    print("-------------------------------------")


def list_duplicates(seq):
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)
    return ((key, locs) for key, locs in tally.items()
            if len(locs) > 1)


def print_list_2d(list_2d):
    print(np.reshape(list_2d, (-1, len(list_2d[0]))))


def print_dup(dup_list, all_reference_list, rpt):
    dup_num = 0
    for dup in dup_list:
        if dup[0] != "none":
            dup_num += 1
            rpt.write("-------------------------------------\n")
            rpt.write("Dup Number: %d\n" % dup_num)
            rpt.write("\n")
            for ind in dup[-1]:
                ref = all_reference_list[ind + 1]
                rpt.write("In %s : %d-%d :\n" % (ref[0], int(ref[1]), int(ref[2])))
                with open(ref[0], 'r') as x:
                    line = x.readlines()
                    for i in range(int(ref[1]) - 1, int(ref[2])):
                        rpt.write('\t' + line[i])
                    # rpt.writelines(line[ref[1]-1:ref[2]])
                    rpt.write("\n")
                # print(reference[ind+1])


main()
