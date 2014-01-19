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
            #if not 'seq_idx' in cur_root or cur_root['seq_idx'] == 0:
            if cur_root == self.root:
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

class LLRB_BSTree(BSTree):
    def rotate_right(self,cur_root = None):
        use_self_root =False
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
        #"count" Must be DEALT WITH
        child["count"] = cur_root["count"]
        if "left" in child:
            cur_root["count"] -= (child["left"]["count"] + 1)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if use_self_root:
            self.root = child
        return child
    def rotate_left(self,cur_root = None):
        use_self_root =False
        if cur_root is None:
            use_self_root = True
            cur_root = self.root
        if not "right" in cur_root:
            return cur_root
        child = cur_root["right"]
        if not "left" in child:
            del cur_root["right"]
        else:
            cur_root["right"] = child["left"]
        child["left"] = cur_root

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #"count" Must be DEALT WITH
        child["count"] = cur_root["count"]
        if "right" in child:
            cur_root["count"] -= (child["right"]["count"] + 1)
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if use_self_root:
            self.root = child
        return child
    def is_red(self,node,which_child):
        if not which_child in node:
            return False
        return node[which_child]['red'] == 1
    def flipcolor(self,node):
        node['red'] = 1
        node['left']['red'] = 0
        node['right']['red'] = 0
    def add(self,node_key):
        def llrb_add_hit_cb(node):
            node['repeat'] += 1
        def llrb_add_miss_cb(node):
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
            sel_node['red'] = 1
        def llrb_add_pass_cb(result,node):
            node['count'] = 1
            if 'left' in node:
                node['count'] = node['left']['count']
            if 'right' in node:
                node['count'] += node['right']['count']

            #In 3-node of a 2-3 tree, we set the children of three sub-nodes as number 0 1 2 as the following:
            #                     |
            #               | A  3-Node |
            #               /     |     \
            #sub-nodes: node 0  node 1  node 2
            #Lean-Left Red Black Tree Patterns
            #   pattern0            pattern1                pattern2
            #       /                  /                      /
            #    *node               node                  *node
            #     /                  /                     /    \
            #   node              *node                  node   node
            #   /                    \
            # node                   node
            patn0_exists = 0
            if 'left' in node:
                if 'left' in node['left']:
                    patn0_exists = 1

            #Pattern 1
            if self.is_red(node,'right') and not self.is_red(node,'left'):
                self.rotate_left(node)
            #Pattern 0
            if patn0_exists == 1 and self.self.is_red(node,'left') and self.is_red(node['left'],'left'):
                self.rotate_right(node)
            #Pattern 2
            if self.is_red(node,'left') and self.is_red(node,'right'):
                self.flipcolor(node)

        self.search(node_key,hit_cb=llrb_add_hit_cb,miss_cb=llrb_add_miss_cb,pass_wayup=llrb_add_pass_cb)
        self.root['red'] = 0#!!! Set Root to Black


if __name__ == '__main__':
    bst = LLRB_BSTree()
    for i in range(0,5):
        bst.add(i)
    print(bst)
    #bst.rotate_right()
    ##bst.travese()
    #print("-------------------------------------\n")
    #print(bst)

    #bst.rotate_left()
    ##bst.travese()
    #print("-------------------------------------\n")
    #print(bst)
