import tkinter
from tkinter.ttk import *
import os
import re
import jellyfish


# -------------------------------------------------------------

def evaluate_boolean_query(query, parts):
    query_words = query.lower().split()

    if "or" in query_words:
        query_words.remove("or")
        for word in query_words:
            if word in parts:
                return True
        return False


    elif "and" in query_words:
        query_words.remove("and")
        for word in query_words:
            if word not in parts:
                return False
        return True


    elif "not" in query_words:
        query_words.remove("not")
        for word in query_words:
            if word in parts:
                return False
        return True

    else:
        return all(word in parts for word in query_words)
# --------------------------------------------------------------------------------
def match_pattern(pattern, word):
    if pattern.startswith('*') and pattern.endswith('*'):
        return pattern[1:-1] in word
    elif pattern.startswith('*'):
        return word.endswith(pattern[1:])
    elif pattern.endswith('*'):
        return word.startswith(pattern[:-1])
    else:
        parts = pattern.split('*')
        if len(parts) == 2:
            return word.startswith(parts[0]) and word.endswith(parts[1])
        else:
            return False


def is_matching(query, words):
    matching_words = []
    for index, word in enumerate(words):
        if match_pattern(query, word):
            matching_words.append((index, word))
    return matching_words


def split_string(s):
    return [''.join(filter(str.isalpha, token)).lower() for token in s.split()]


def read_data_in_file(file):
    return file.readline().strip()


# ---------------------------
from nltk.stem import PorterStemmer

# -----------------------------------
ps = PorterStemmer()
dir(ps)

T = [[], [], [], [], [], [], [], [], [], []]
T2 = [[], [], [], [], [], [], [], [], [], []]
array = []
array1 = []
found = False

f = open("C:/doc/coll.txt", "r")
coll = f.read()

# --------------------------------
arr = []
f_w_w = []
# ----------------------------------
fp = "C:/doc/"
files = [fp + "D1.txt", fp + "D2.txt", fp + "D3.txt", fp + "D4.txt",
         fp + "D5.txt", fp + "D6.txt", fp + "D7.txt", fp + "D8.txt", fp + "D9.txt", fp + "D10.txt"]

root = tkinter.Tk()
root.title("AHU SEARCH ENGIN")
root.geometry('350x200')
for i in range(3):
    root.columnconfigure(i, weight=1, minsize=75)
    root.rowconfigure(i, weight=1, minsize=50)
lbl = Label(root, text="AHU SEARCH")
lbl.grid(column=1, row=0)
lbl1 = Label(root, text="")
lbl1.grid(column=2, row=1)

txt = Entry(root, width=20)
txt.grid(column=1, row=1)


def click1():
    res = str((txt.get()))
    if '"' in res:
        def extract_words(fn):

            M = res.strip('\"')
            with open(fn, 'r') as file:
                content = file.read()
                words = list(re.findall(M, content))
                fn = os.path.basename(fn)
                if words:
                    # print(f"Words found in {fn}: {words} {len(words)}")      # طباعة اسم الملف
                    arr.append(f"{len(words) / len(content)}--{fn}")
                    return fn
                return None

        for fn in files:
            found = extract_words(fn)
            if found:
                f_w_w.append(found)
        arr.sort(reverse=True)
        for fn in arr:
            lbl.configure(text=arr)
        print(arr)
    elif "*" in res:
        arr1=[]
        files_name = files

        query = res.lower()
        found = False

        for filename in files_name:
            with open(filename) as file:
                line = read_data_in_file(file)
                words = split_string(line)
                matching_words = is_matching(query, words)
                if matching_words:
                    found = True
                    for index, word in matching_words:

                        if filename == filename:
                            break

                    lbl.configure(text=((len(matching_words)/len(filename)),filename))
                    print(((len(matching_words)/len(filename)),filename))

        print(word)

        if not found:
            print("No matching words found in files.")

#------------------------------------------------------------------------------
    elif any(x in res for x in ["and", "or", "not"]):  #تم تعريف متغير يحتوي عل حالات الكويري لفحص الادخال في حال تواجد احدى حالات الكويري

        files_name = files
        query = res
        flag = 0

        for filename in files_name:
            with open(filename) as file:
                line = read_data_in_file(file)#تم تعريف متغير و حفظ  فيه الداتا بعد قراتها
                parts = split_string(line) #تم ارسال الداتا بعد قراتها لفنكشن سبلت
                if evaluate_boolean_query(query, parts):#عملية مقارنة المدخل مع الداتا بعد ارسالها فنكشن في حال تحقق الشرط
                    print("Matching words found in file:", filename)#يطبع اسم الفايل
                    flag += 1
        if flag == 0:
            print("No matching words found in files.")

#--------------------------------------------------------------------------------------
    elif res in coll:  # تم تعريف كوكشن و وضع فيها كل الدوكيومنت المطلوبة لفحص اذا الكلمة موجودة
        fre = 0
        for i in range(10):
            f = open(files[i], "r")
            u = f.read()
            f.close()
            u = u.split()
            T.insert(i, u)

        for i in range(10):
            coun = len(T[i])
            array.clear()
            for j in range(coun):
                index = T[9][j]
                temp1 = (ps.stem(index))
                array.append(temp1)
                T.append(array)

        for i in range(10):
            for j in range(len(T[i])):
                if res == T[i][j]:
                    fre = fre + 1
            if fre > 0:
                array1.append(f"{fre / len(T[i])} DOC{i + 1}")
                fre = 0

        array1.sort(reverse=True)
        lbl.configure(text=array1)
        print(array1)
    else:
        fre = 0
        for i in range(10):
            f = open(files[i], "r")
            u = f.read()
            f.close()
            u = u.split()
            T.insert(i, u)

        for i in range(10):
            coun = len(T[i])
            array.clear()
            for j in range(coun):
                index = T[i][j]
                temp1 = (ps.stem(index))
                array.append(temp1)
                T2[i].append(array)

        for i in range(10):
            for j in range(len(T[i])):
                val = T[i][j]
                temp1 = jellyfish.soundex(res)
                temp2 = jellyfish.soundex(val)
                if temp2 == temp1:
                    fre = fre + 1
                    gl=val
            if fre > 0:
                array1.append(f"{fre / len(T[i])} DOC{i + 1}")
                fre = 0

        array1.sort(reverse=True)
        print(array1)
        lbl.configure(text=array1)
        lbl1.configure(text="Did you mean ="+gl)
        array1.clear()


btn = Button(root, text="SEARCH", command=click1)
btn.grid(column=1, row=2)
root.mainloop()
