#!/usr/bin/python
class BSTree:
	def __init__(self,a_go_first = lambda a,b:a>b):
		self.a_go_first = a_go_first
		self.root = {}
	def search(self,node_key,cur_root = None,hit_cb = None,miss_cb = None,pass_cb = None):
		if cur_root is None:
			cur_root = self.root

		if node_key == cur_root['key']:
			if not hit_cb is None
				hit_cb(cur_root)
			return True,cur_root
		result,ret_node = False,cur_root
		pass_thru = False 
		if 'left' in cur_root and node_key < cur_root['key']:
			result,ret_node = search(cur_root['left'],node_key)
			pass_thru = True
		if 'right' in cur_root and node_key > cur_root['key']:
			result,ret_node = search(cur_root['right'],node_key)
			pass_thru = True
		#If runs here, it means no item has been found
		if pass_thru:
			pass_cb(pass_thru,ret_node)
		else
			if not miss_cb is None
				miss_cb(ret_node)
		return result,ret_node

	#def select(self,node_key,cur_root = None):
	def add(self,node_key):
		def add_hit_cb(node):
			node['repeat'] += 1
		def add_miss_cb(node):
			if node_key < node['key']:
				node['left'] = {'key':node_key}
			else#>
				node['right'] = {'key':node_key}
			node['repeat'] = 1
			node['count'] = 1
		def add_pass_cb(result,node):
			node['count'] = node['left']['count'] + node['right']['count']
		search(self,node_key,hit_cb=add_hit_cb,miss_cb=add_miss_cb,pass_cb=add_pass_cb)
	def travese(self,cur_root = None):
		if cur_root is None:
			cur_root = self.root
		if not 'left' in cur_root and not 'right' in cur_root:
			return [cur_root['key']]
		if 'left' in cur_root:
			l_subtree = travese(self,cur_root['left'])
		if 'right' in cur_root:
			r_subtree = travese(self,cur_root['right'])
		return l_subtree + [cur_root['key']] + r_subtree
	#def floor(self,node_key):

	#def __str__(self):
	#    whole_tree = ""
	#    tree = []
	#    cur_layer = []
	#    nxt_layer_end_cnt = 0
	#    for i,v in enumerate(tree2disp):
	#        cur_layer.append(v)
	#        if i == nxt_layer_end_cnt or i == len(tree2disp)-1:
	#            nxt_layer_end_cnt = i*2+2
	#            tree.append(cur_layer)
	#            cur_layer = []
	#    space_cnt = 0
	#    layer = len(tree)
	#    bottom_width = 2**layer
	#    for i,vln in enumerate(tree):
	#        space = " "*3*((bottom_width-1) // (2**i))
	#        curr_layer  = " "*3*((bottom_width-1) // (2**i) //2)
	#        #print(space)
	#        #print(curr_layer)
	#        for i,v in enumerate(vln):
	#            curr_layer = curr_layer + ("%3d" %  v)
	#            if i< len(vln) - 1:
	#                curr_layer = curr_layer + space
	#        curr_layer += "\n"
	#        print(curr_layer)

if __name__ == '__main__':
	h = Node()
	n = Node()
	n.key = 200
	h.nxt = n
	h.key = 100
	print(h.nxt.key)
