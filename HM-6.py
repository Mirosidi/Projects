from pathlib import Path
import shutil
import sys
import os
import re

TRANS = {
    1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D',
    1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I',
    1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N',
    1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T',
    1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS',
    1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y',
    1100: '', 1068: '', 1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE',
    1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'
}
dict_sufixes = {
    '.ZIP': 'archives', '.GZ': 'archives', '.TAR': 'archives',
    '.AVI': 'video', '.MP4': 'video', '.MOV': 'video', '.MKV': 'video',
    '.MP3': 'audio', '.OGG': 'audio', '.WAV': 'audio', '.AMR': 'audio',
    '.DOC': 'documents', '.DOCX': 'documents', '.TXT': 'documents', '.PDF': 'documents', '.XLSX': 'documents',
    '.PPTX': 'documents',
    '.JPEG': 'images', '.PNG': 'images', '.JPG': 'images', '.SVG': 'images',
    'others': 'others'
}
Name_dir = ('archives', 'video', 'audio', 'documents', 'images', 'others')
list_name_all_file = []
def normalize(file_name):
    patern = r"\W"
    replace = "_"
    normalize_file_name = re.sub(patern, replace, file_name)
    new_file_name = normalize_file_name.translate(TRANS)
    return new_file_name
def unpack_archive(new_path_file_arhive, extract_arhive_dir_name, format_unpack_arhive):
    try:
        shutil.unpack_archive(new_path_file_arhive, extract_arhive_dir_name,f'{format_unpack_arhive}')
    except:
        print(f'Bad arhive was delete <{new_path_file_arhive}>')
        os.remove(new_path_file_arhive)
def replace_files(root_path, path_file):
    name_file = normalize(path_file.stem)
    suf_file = path_file.suffix
    category = dict_sufixes.get(suf_file.upper(), 'others')
    new_path_dir = Path(f'{root_path}/{category}')
    if not new_path_dir.exists():
        new_path_dir.mkdir()
    file_name_curent = f'{name_file}{suf_file}'
    list_name_all_file.append(file_name_curent)
    path_file.replace(new_path_dir / f"{name_file}{suf_file}")
    if suf_file.upper() in ('.ZIP', '.GZ', '.TAR'):
        new_path_file_arhive = Path(f'{new_path_dir}/{name_file}{suf_file.lower()}')
        extract_arhive_dir_name = Path(f'{new_path_dir}/{name_file}')
        format_unpack_arhive = re.sub(r'\.', '', suf_file.lower())
        unpack_archive(new_path_file_arhive, extract_arhive_dir_name, format_unpack_arhive)
    return list_name_all_file
def lists_file_sort(list_name_all_file, root_path):
    list_all_known_sufix = []
    list_all_unknown_sufix = []
    list_file_archives = []
    list_file_video = []
    list_file_audio = []
    list_file_documents = []
    list_file_images = []
    list_file_others = []
    suff_images = ('JPEG', 'PNG', 'JPG', 'SVG')
    suff_video = ('AVI', 'MP4', 'MOV', 'MKV')
    suff_documents = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    suff_audio = ('MP3', 'OGG', 'WAV', 'AMR')
    suff_arhives = ('ZIP', 'GZ', 'TAR')
    for name in list_name_all_file:
        suff = name.split('.')
        if suff[1].upper() in suff_audio:
            list_file_audio.append(name)
            list_all_known_sufix.append(suff[1])
        elif suff[1].upper() in suff_video:
            list_file_video.append(name)
            list_all_known_sufix.append(suff[1])
        elif suff[1].upper() in suff_documents:
            list_file_documents.append(name)
            list_all_known_sufix.append(suff[1])
        elif suff[1].upper() in suff_images:
            list_file_images.append(name)
            list_all_known_sufix.append(suff[1])
        elif suff[1].upper() in suff_arhives:
            list_file_archives.append(name)
            list_all_known_sufix.append(suff[1])
        else:
            list_file_others.append(name)
            list_all_unknown_sufix.append(suff[1])
    list_all_known_sufix = list(set(list_all_known_sufix))
    list_all_unknown_sufix = list(set(list_all_unknown_sufix))
    path_info_file = Path(f"{root_path}/file_info_in_dir.txt")
    if not path_info_file.is_file():
        with open(path_info_file, "a") as fh:
            ...
    tab = "\t" * 5
    with open(path_info_file, 'w') as fh:
        fh.writelines(f'\n{tab}List of extensions known to the script that were in the folder :\n\n{list_all_known_sufix}\n\n')
        fh.writelines(f'{tab}List of extensions unknown to the script that were in the folder :\n\n{list_all_unknown_sufix}\n\n')
        fh.writelines(f'{tab}List of all Music files that were in the folder :\n\n{list_file_audio}\n\n')
        fh.writelines(f'{tab}List of all video files that were in the folder :\n\n{list_file_video}\n\n')
        fh.writelines(f'{tab}List of all document files that were in the folder :\n\n{list_file_documents}\n\n')
        fh.writelines(f'{tab}List of all photo files in the folder :\n\n{list_file_images}\n\n')
        fh.writelines(f'{tab}A list of all the ARC files that were in the folder :\n\n{list_file_archives}\n\n')
        fh.writelines(f'{tab}A list of all the Unknown files that were in the folder :\n\n{list_file_others}\n\n')
def sort_dir(root_path, path):
    try:
        for item in path.iterdir():
            if item.is_file():
                replace_files(root_path, item)
            if item.is_dir():
                if not item.stem in Name_dir:
                    sort_dir(root_path, item)
                if len(os.listdir(item)) == 0:
                    item.rmdir()
    except:
        pass
    lists_file_sort(list_name_all_file, root_path)
def main():
    try:
        root_path = Path(sys.argv[1])
        path = Path(sys.argv[1])
        sort_dir(root_path, path)
    except:
        print(' \nYou did not specify the path to the folder to be sorted')
if __name__ == '__main__':
    main()