#!/usr/bin/python
#from dat_gen import get_data
from random import randrange
from sys import argv
import argparse

class sort_mgr:
    sort_names = []
    @staticmethod
    def add2mgr(sort_f):
        setattr(sort_mgr,sort_f.__name__,staticmethod(sort_f))
        sort_mgr.sort_names.append(sort_f.__name__)
        return sort_f
    def call_sort(self,sort_name):
        return getattr(self,sort_name)
###################################################
#Insert Sort/Basic Insert Sort
@sort_mgr.add2mgr
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
#Merge Sort/Basic Merge Sort
#Top-Down Implementation
@sort_mgr.add2mgr
def merge_sort_t2b(_sort_A,a_go_first = lambda a,b:a>b):
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
@sort_mgr.add2mgr
def merge_sort_b2t(_sort_A,a_go_first = lambda a,b:a>b):
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
#Exchange Sort/Bubble sort
@sort_mgr.add2mgr
def bubble_sort(_sort_A,a_go_first = lambda a,b: a>b):
    for i in range(len(_sort_A)):
        for j in range(len(_sort_A)-1-i):
            if not a_go_first(_sort_A[j],_sort_A[j+1]):
                _sort_A[j],_sort_A[j+1] = _sort_A[j+1],_sort_A[j]
        #print(_sort_A)

###################################################
#Selection Sort/Basic Selection Sort
@sort_mgr.add2mgr
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
#Selection Sort/Heap Sort
def disp_in_tree(tree2disp):
    whole_tree = ""
    tree = []
    cur_layer = []
    nxt_layer_end_cnt = 0
    for i,v in enumerate(tree2disp):
        cur_layer.append(v)
        if i == nxt_layer_end_cnt or i == len(tree2disp)-1:
            nxt_layer_end_cnt = i*2+2
            tree.append(cur_layer)
            cur_layer = []
    space_cnt = 0
    layer = len(tree)
    bottom_width = 2**layer
    for i,vln in enumerate(tree):
        space = " "*3*((bottom_width-1) // (2**i))
        curr_layer  = " "*3*((bottom_width-1) // (2**i) //2)
        #print(space)
        #print(curr_layer)
        for i,v in enumerate(vln):
            curr_layer = curr_layer + ("%3d" %  v)
            if i< len(vln) - 1:
                curr_layer = curr_layer + space
        curr_layer += "\n"
        print(curr_layer)

def chk_heapify(_heap_A,a_go_first = lambda a,b: a>b):
    for i,v in enumerate(_heap_A):
        for j in range(1,3):
            if (i*2+j) < len(_heap_A) and not a_go_first(_heap_A[i],_heap_A[2*i+j]):
                if not _heap_A[i] == _heap_A[2*i+j]:
                    print("Heap rule violation at root:%3d[%0d] & leaf:%3d[%0d]"% (_heap_A[i],i,_heap_A[2*i+j],2*i+j))

def heapify_b2t_iter(_heap_A,a_go_first = lambda a,b: a>b):
                
    #print("-"*70)
    #disp_in_tree(_heap_A)
    def shift_down(_heap_A,nxt_root,a_go_first = lambda a,b: a>b):
        while nxt_root < len(_heap_A):
            k = nxt_root
            for j in range(1,3):
                #Out of index range
                if 2*k+j >= len(_heap_A):
                    break
                if not a_go_first(_heap_A[nxt_root],_heap_A[2*k+j]):
                    nxt_root = 2*k+j
            # To terminate the outter while loop 
            if nxt_root == k:
                return
            else:
                _heap_A[k],_heap_A[nxt_root] = _heap_A[nxt_root],_heap_A[k]

    for i in reversed(range((len(_heap_A)-2)//2+1)):
        nxt_root = i
        shift_down(_heap_A,nxt_root,a_go_first)
    #print("="*30)
    #disp_in_tree(_heap_A)
    #print("-"*70)
    chk_heapify(_heap_A,a_go_first)
    return shift_down

@sort_mgr.add2mgr
def heapsort_b2t(_heap_A,a_go_first = lambda a,b: a>b):
    to_heapify = _heap_A[:]
    shift_down = heapify_b2t_iter(to_heapify,a_go_first)
    for i in range(len(_heap_A)):
        _heap_A[i] = to_heapify[0]
        if i < len(_heap_A)-1:
            #swap the root and the least leaf in heap
            to_heapify[0] = to_heapify[-1]
            to_heapify = to_heapify[:-1]
            shift_down(to_heapify,0,a_go_first)
        #print("="*30)
        #disp_in_tree(to_heapify)

def heapify_t2b_iter(_heap_A,a_go_first = lambda a,b: a>b):
    #print("-"*70)
    #disp_in_tree(_heap_A)
    def shiftup(_heap_A,root,leaf,a_go_first = lambda a,b: a>b):
        while root >= 0:
            if not a_go_first(_heap_A[root],_heap_A[leaf]):
                _heap_A[leaf],_heap_A[root] = _heap_A[root],_heap_A[leaf]
                leaf,root = root,(root-1)//2
            else:
                break
        return root,leaf
    for i in range(1,len(_heap_A)):
        root = (i-1)//2
        leaf = i
        root,leaf = shiftup(_heap_A,root,leaf,a_go_first)
    #print("="*30)
    #disp_in_tree(_heap_A)
    #print("-"*70)
    chk_heapify(_heap_A,a_go_first)
    return shiftup

@sort_mgr.add2mgr
def heapsort_t2b(_heap_A,a_go_first = lambda a,b: a>b):
    to_heapify = _heap_A[:]
    for i in range(len(_heap_A)):
        heapify_t2b_iter(to_heapify,a_go_first)
        _heap_A[i] = to_heapify[0]
        to_heapify = to_heapify[1:]
        
###################################################
#Starting the test program
def test_bench(mgr,sel,swap_method):
    sort_A = [randrange(0,40,1) for x in range(23)]

    before_sort = sort_A[:]
    print("Before sorting",sort_A)
    before_sort.sort(reverse=swap_method[1])
    print("Expect        ",before_sort)
    mgr.call_sort(sel)(sort_A,swap_method[0]) 

    print("After sorting ",sort_A)
    for i in range(len(before_sort)):
        if before_sort[i] != sort_A[i]:
            print("Mismatch@",i," --- expected:",before_sort[i],"observed:",sort_A[i])

swap_method={"ascend":(lambda a,b:a<b,False),
            "descend":(lambda a,b:a>b,True)}

mgr = sort_mgr()
parser = argparse.ArgumentParser(description = "A Python script implementing lots of sorting algorithm") 
parser.add_argument('sort_algorithm',choices = mgr.sort_names,help = "available sorting methords")
parser.add_argument('--direction','-d',choices=["ascend","descend"],help="the direction of sorting result")
args = parser.parse_args()
test_bench(mgr,args.sort_algorithm,swap_method[args.direction])
