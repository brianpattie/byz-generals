class OrderTree():

    def __init__(self, height):
        self.root = {}
        self.height = height

    def insert(self, order, location_list):
        #TODO: must revisit this.  Where do we store the commander's order?
        if len(location_list) = height:
            self.recursive_insert(self.root, order, location_list)
        else:
            print('Error: location_list length must equal tree height')

    def recursive_insert(self, dict, order, location_list):
        # Base Case: add order at this level
        print(location_list)
        if len(location_list) == 1:
            dict[location_list[0]]['value'] = order
        # Must go deeper
        else:
            #
            if location_list[0] not in dict.keys():
                dict[location_list[0]] = {}
            self.recursive_insert(dict[location_list[0]], order, location_list[1:])

    def decision(self):
        return self.recursive_decision(self.root, 0)

    def recursive_decision(self, dict, depth):
        if depth == self.height - 1:
            majority(dict)
        for key in dict:



o = Ordertree()
o.insert(1, [0,1,2,3])
o.insert(1, [0,1,2,4])
o.insert(1, [1,1,2,3])
o.insert(1, [1,1,2,4])



print(o.root[0][1][2])
