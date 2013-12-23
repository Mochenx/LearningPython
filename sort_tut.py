#!/usr/bin/python
#from dat_gen import get_data
from random import randrange
from sys import argv
import argparse

###################################################
#Insert sort
def insert_sort(_sort_A,a_go_first = lambda a,b:a>b):
    for v_with_idx in enumerate(_sort_A[:]):
        for _before_v in enumerate(_sort_A[0:v_with_idx[0]]):
            #print(_sort_A)
            #print(_before_v,v_with_idx)
            if a_go_first(v_with_idx[1],_before_v[1]):
                _v = _sort_A.pop(v_with_idx[0])
                _sort_A.insert(_before_v[0],_v)
                break
###################################################
#Merge sort
#Top-Down Implementation
def top_down_merge_sort(_sort_A,a_go_first = lambda a,b:a>b):
    _sort_A[:] = top_down_split_merge(_sort_A[:],a_go_first)
def top_down_split_merge(_sort_A,a_go_first = lambda a,b:a>b):
    if len(_sort_A) < 2:
        return _sort_A
    
    return top_down_merge(  top_down_split_merge(_sort_A[0:len(_sort_A)//2],a_go_first),
                            top_down_split_merge(_sort_A[len(_sort_A)//2:],a_go_first),
                            a_go_first)
def top_down_merge(_sort_left,_sort_right,a_go_first = lambda a,b:a>b):
    new_array = []
    total_size = len(_sort_left) + len(_sort_right)
    for i in range(total_size):
        if (len(_sort_left) != 0) and \
                (len(_sort_right) == 0 or a_go_first(_sort_left[0],_sort_right[0])):
            new_array.append(_sort_left.pop(0))
        else:
            new_array.append(_sort_right.pop(0))
    return new_array

#Down-Top Implementation
def down_top_merge_sort(_sort_A,a_go_first = lambda a,b:a>b):
    size = len(_sort_A)
    width = 1
    while (2*width)//size < 2:
        s = 0
        while s < size:
            new_array = []
            _sort_left = _sort_A[s:s+width]
            _sort_right = _sort_A[s+width:s+2*width]
            total_width = len(_sort_left) + len(_sort_right)
            #print(_sort_left)
            #print(_sort_right)
            #print("--------------")
            for n in range(0,total_width):
                if (len(_sort_left) != 0) and \
                        (len(_sort_right) == 0 or a_go_first(_sort_left[0],_sort_right[0])):
                    new_array.append(_sort_left.pop(0))
                else:
                    new_array.append(_sort_right.pop(0))
            _sort_A[s:s+2*width] = new_array
            s += (2*width)
        #print("===================")
        width *= 2
###################################################
#Selection Sort
def selection_sort(_sort_A,a_go_first = lambda a,b: a>b):
    for i,item_prev in enumerate(_sort_A[:]):
        sel_idx = i
        for j,item_curr in enumerate(_sort_A[i+1:]):
            if not a_go_first(_sort_A[sel_idx],item_curr):
                sel_idx = j+(i+1)
                #print(_sort_A[sel_idx])
                #print(sel_idx)
        _sort_A[i],_sort_A[sel_idx] = _sort_A[sel_idx],_sort_A[i]
        #print(_sort_A)
        #print("--------------")

###################################################
#Bubble sort
def bubble_sort(_sort_A,a_go_first = lambda a,b: a>b):
    for i in range(len(_sort_A)):
        for j in range(len(_sort_A)-1-i):
            if not a_go_first(_sort_A[j],_sort_A[j+1]):
                _sort_A[j],_sort_A[j+1] = _sort_A[j+1],_sort_A[j]
        #print(_sort_A)


###################################################
#Starting the test program
def test_bench(sort_table,sel,swap_method):
    sort_A = [randrange(0,40,1) for x in range(23)]

    before_sort = sort_A[:]
    print("Before sorting",sort_A)
    before_sort.sort(reverse=swap_method[1])
    print("Expect        ",before_sort)
    sort_table[sel](sort_A,swap_method[0])

    print("After sorting ",sort_A)
    for i in range(len(before_sort)):
        if before_sort[i] != sort_A[i]:
            print("Mismatch@",i," --- expected:",before_sort[i],"observed:",sort_A[i])

swap_method={"ascend":(lambda a,b:a<b,False),
            "descend":(lambda a,b:a>b,True)}
sort_table={"insert":insert_sort,
            "merge_t2b":top_down_merge_sort,
            "merge_b2t":down_top_merge_sort,
            "selection":selection_sort,
            "bubble":bubble_sort}
parser = argparse.ArgumentParser(description = "A Python script implementing lots of sorting algorithm") 
parser.add_argument('sort_algorithm',choices=["insert","merge_t2b","merge_b2t","selection","bubble"],help = "available sorting methords")
parser.add_argument('--direction','-d',choices=["ascend","descend"],help="the direction of sorting result")
args = parser.parse_args()
test_bench(sort_table,args.sort_algorithm,swap_method[args.direction])
#if len(argv) == 3:
#    if argv[1] in ["insert","merge_t2b","merge_b2t","selection","bubble"] and \
#            argv[2] in ["ascend","descend"]:
#        test_bench(sort_table,argv[1],swap_method[argv[2]])
#    else:
#        print("illegal arguments",argv[1]," and ",argv[2])
#else:
#    print("Usage:sort_tut sort_method ascend/descend")
#    print("sort_method:")
#    print("\t1. insert:execute insert sort")
#    print("\t2. merge :execute merge_[b2t/t2b]  sort")
#    print("\t3. selection :execute selection  sort")
#    print("\t4. bubble :execute bubble  sort")
#
