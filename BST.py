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
		if 'left' in cur_root and node_key < cur_root['key']:
			if 'pass_waydown' in key_cbs:
				key_cbs['pass_waydown'](cur_root['left'])
			result,ret_node = self.search(node_key,cur_root['left'],key_cbs)
			pass_thru = True
		if 'right' in cur_root and node_key > cur_root['key']:
			if 'pass_waydown' in key_cbs:
				key_cbs['pass_waydown'](cur_root['right'])
			result,ret_node = self.search(node_key,cur_root['right'],key_cbs)
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
				if node_key < node['key']:
					node['left'] = {'key':node_key}
					sel_node = node['left']
				else:#>
					node['right'] = {'key':node_key}
					sel_node = node['right']
			sel_node['repeat'] = 1
			sel_node['count'] = 1
		def add_pass_cb(result,node):
			node['count'] = node['left']['count'] + node['right']['count']
		self.search(node_key,hit_cb=add_hit_cb,miss_cb=add_miss_cb,pass_wayup=add_pass_cb)

	def travese(self,cur_root = None,**kargs):
		if cur_root is None:
			cur_root = self.root
		if not 'left' in cur_root and not 'right' in cur_root:
			if 'leaf' in kargs:
				kargs['leaf'](cur_root)
			return [cur_root['key']]
		l_subtree = []
		r_subtree = None
		if 'pass_waydown' in kargs:
			kargs['pass_waydown'](cur_root)
		if 'left' in cur_root:
			l_subtree = self.travese(cur_root['left'])
		if 'right' in cur_root:
			r_subtree = self.travese(cur_root['right'])
		if 'pass_wayup' in kargs:
			kargs['pass_wayup'](cur_root)
		print(cur_root)
		l_subtree.extend([cur_root['key']])
		if not r_subtree is None:
			l_subtree.extend(r_subtree)
		return l_subtree
	def layerify(self):
		depth = 0
		all_layers = []
		def waydown(cur_root):
			depth += 1
		def wayup(cur_root):
			depth -= 1
		def leaf(cur_root):
			depth -= 1
		travese()
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
	bst = BSTree()
	bst.add(1)
	bst.add(0)
	bst.travese()
