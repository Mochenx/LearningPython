#!/usr/bin/python
class BSTree:
    def __init__(self,a_go_first = lambda a,b:a>b):
        self.a_go_first = a_go_first
        self.root = {}
    def search(self,node_key,cur_root = None,**key_cbs):
        if cur_root is None:
            cur_root = self.root

        if 'key' in cur_root and node_key == cur_root['key']:
            if 'hit_cb' in key_cbs:
                key_cbs['hit_cb'](cur_root)
            return True,cur_root
        result,ret_node = False,cur_root
        pass_thru = False 
        if 'left' in cur_root and self.a_go_first(node_key , cur_root['key']):
            if 'pass_waydown' in key_cbs:
                key_cbs['pass_waydown'](cur_root['left'])
            result,ret_node = self.search(node_key,cur_root['left'],**key_cbs)
            pass_thru = True
        if 'right' in cur_root and not self.a_go_first(node_key , cur_root['key']):
            if 'pass_waydown' in key_cbs:
                key_cbs['pass_waydown'](cur_root['right'])
            result,ret_node = self.search(node_key,cur_root['right'],**key_cbs)
            pass_thru = True
        #If runs here, it means no item has been found
        if pass_thru:
            if 'pass_wayup' in key_cbs:
                key_cbs['pass_wayup'](pass_thru,ret_node)
        else:
            if 'miss_cb' in key_cbs:
                key_cbs['miss_cb'](ret_node)
        return result,ret_node

    #def select(self,node_key,cur_root = None):
    def add(self,node_key):
        def add_hit_cb(node):
            node['repeat'] += 1
        def add_miss_cb(node):
            if not 'key' in node:
                node['key'] = node_key
                sel_node = node
            else:
                if self.a_go_first(node_key , node['key']):
                    node['left'] = {'key':node_key}
                    sel_node = node['left']
                else:#>
                    node['right'] = {'key':node_key}
                    sel_node = node['right']
            sel_node['repeat'] = 1
            sel_node['count'] = 1
        def add_pass_cb(result,node):
            node['count'] = 1
            if 'left' in node:
                node['count'] = node['left']['count']
            if 'right' in node:
                node['count'] += node['right']['count']
        self.search(node_key,hit_cb=add_hit_cb,miss_cb=add_miss_cb,pass_wayup=add_pass_cb)

    def travese(self,cur_root = None,**kargs):
        if cur_root is None:
            cur_root = self.root
        if not 'left' in cur_root and not 'right' in cur_root:
            if 'leaf' in kargs:
                kargs['leaf'](cur_root)
            return [cur_root['key']]* cur_root['repeat']
        l_subtree = []
        r_subtree = None
        if 'pass_waydown' in kargs:
            kargs['pass_waydown'](cur_root)
        if 'left' in cur_root:
            l_subtree = self.travese(cur_root['left'],**kargs)
        if 'right' in cur_root:
            r_subtree = self.travese(cur_root['right'],**kargs)
        if 'pass_wayup' in kargs:
            kargs['pass_wayup'](cur_root)
        #print(cur_root)
        l_subtree.extend([cur_root['key']] * cur_root['repeat'])
        if not r_subtree is None:
            l_subtree.extend(r_subtree)
        return l_subtree
    def layerify(self):
        self.depth = 1
        self.max_depth = 0
        all_in_layers = {}
        def waydown(cur_root):
            #Root
            if not 'seq_idx' in cur_root or cur_root['seq_idx'] == 0:
                cur_root['seq_idx'] = 0
                all_in_layers[0] = cur_root

            if 'left' in cur_root:
                cur_root['left']['seq_idx'] = cur_root['seq_idx'] * 2+1
                all_in_layers[cur_root['seq_idx'] * 2+1] = cur_root['left']
            if 'right' in cur_root:
                cur_root['right']['seq_idx'] = cur_root['seq_idx'] * 2+2
                all_in_layers[cur_root['seq_idx'] * 2+2] = cur_root['right']
            self.depth += 1
        def wayup(cur_root):
            self.depth -= 1

        def leaf(cur_root):
            if self.max_depth < self.depth:
                self.max_depth = self.depth
        self.travese(self.root,pass_waydown=waydown,pass_wayup=wayup,leaf=leaf)
        return all_in_layers
    #def floor(self,node_key):

    def __str__(self):
        whole_tree = ""
        tree = []
        cur_layer = []
        nxt_layer_end_cnt = 0
        tree2disp = self.layerify()
        range_size = 0
        for i in range(self.max_depth):
            range_size += 2**i
        for i in range(range_size):
            if i in tree2disp:
                cur_layer.append(tree2disp[i]['key'])
            else:
                cur_layer.append(-1)
            if i == nxt_layer_end_cnt or i == (range_size-1):#or i == len(tree2disp)-1:
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
                if v == -1:
                    curr_layer = curr_layer + ("   ")
                else:
                    curr_layer = curr_layer + ("%3d" %  v)
                if i< len(vln) - 1:
                    curr_layer = curr_layer + space
            curr_layer += "\n"
            whole_tree += curr_layer
        return whole_tree

    def rotate_left(self,cur_root = None):
        if cur_root is None:
            use_self_root = True
            cur_root = self.root

        if not 'left' in cur_root:
            return cur_root
        child = cur_root['left']
        if not 'right' in child:
            del cur_root['left']
        else:
            cur_root['left'] = child['right']
        child['right'] = cur_root
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #seq_idx & count Must be DEALT WITH
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if use_self_root:
            self.root = child
        return child
    

if __name__ == '__main__':
    bst = BSTree()
    bst.add(0)
    bst.add(1)
    bst.add(2)
    bst.add(5)
    #bst.add(8)
    #bst.add(7)
    #bst.add(9)
    print(bst)
    bst.rotate_left()
    #bst.travese()
    print("-------------------------------------\n")
    print(bst)
