import sys
import threading
import queue

class OrderNode():

    def __init__(self, value):
        self.value = value
        self.dict = {}

    # Returns the order (a string)
    def majority(self):

        # Perform majority on all child nodes
        for k in self.dict.keys():
            self.dict[k].majority()

        orders = [self.value]
        counts = [1]

        for k in self.dict.keys():

            o = self.dict[k]

            if o.value not in orders:
                orders.append(o.value)
                counts.append(1)
            else:
                counts[orders.index(o.value)] += 1

        # Return the majority winner, or 'RETREAT' if there's a tie
        m = max(counts)
        if counts.count(m) == 1:
            self.value = orders[counts.index(m)]
        else:
            self.value = 'RETREAT'

    # Must be rewritten as a method of OrderNode
    def insert(self, order, order_path):

        if len(order_path) == 0:
            self.value = order
            return

        if order_path[0] not in self.dict.keys():
            self.dict[order_path[0]] = OrderNode(None)

        self.dict[order_path[0]].insert(order, order_path[1:])


class OrderTree():

    def __init__(self):
        self.root = OrderNode(None)
        self.num_nodes = 0

    def insert(self, order, order_path):
        self.root.insert(order, order_path[1:])
        self.num_nodes += 1

    def majority(self):
        self.root.majority()
        return self.root.value

class Message():

    def __init__(self, order, order_path, r_level):
        self.order = order
        self.order_path = order_path
        self.r_level = r_level

    def copy(self):
        return Message(self.order, self.order_path[:], self.r_level)

    def print(self):
        print(self.order + " " + str(self.order_path) + " " + str(self.r_level))


class General(threading.Thread):

    def __init__(self, id, loyal, queues, expected):
        threading.Thread.__init__(self)
        self.id = id
        self.loyal = loyal
        self.queues = queues
        self.expected = expected
        self.ordertree = OrderTree()

    def run(self):
        if self.id == 0:
            msg = self.queues[self.id].get()
            self.ordertree.insert(msg.order, msg.order_path)
            if self.loyal:
                self.loyal_relay(msg)
            else:
                self.traitor_relay(msg)

            self.print_action(self.ordertree.majority())

        else:
            while self.ordertree.num_nodes < self.expected:
                msg = self.queues[self.id].get()
                self.ordertree.insert(msg.order, msg.order_path)
                if msg.r_level > 0:
                    if self.loyal:
                        self.loyal_relay(msg)
                    else:
                        self.traitor_relay(msg)

            self.print_action(self.ordertree.majority())

    def loyal_relay(self, msg):

        # Copy the message, add yourself to the order's history, decrement the recursion level
        new_msg = msg.copy()
        new_msg.order_path.append(self.id)
        new_msg.r_level -= 1

        # Send a copy to every general not in the message's history
        for i in range(0, len(queues)):
            if i not in new_msg.order_path:
                self.queues[i].put(new_msg.copy())


    def traitor_relay(self, msg):
        # Copy the message, add yourself to the order's history, decrement the recursion level
        loyal_msg = msg.copy()
        loyal_msg.order_path.append(self.id)
        loyal_msg.r_level -= 1

        # Same as above, but also lie about the order
        traitor_msg = msg.copy()
        traitor_msg.order_path.append(self.id)
        traitor_msg.r_level -= 1
        traitor_msg.order = self.flip(msg.order)

        # Send a copy to every general not in the message's history
        for i in range(0, len(queues)):
            if i not in loyal_msg.order_path:
                if i % 2 == 1:
                    self.queues[i].put(loyal_msg.copy())
                else:
                    self.queues[i].put(traitor_msg.copy())

    def flip(self, order):
        if order == 'ATTACK':
            return 'RETREAT'
        else:
            return 'ATTACK'

    def print_action(self, action):
        if self.loyal:
            print("Loyal General   " + str(self.id) + " took action " + action)
        else:
            print("Traitor General " + str(self.id) + " took action " + action)

def expected(num_gen, r_level):

    def r_expected(num_gen, r_level):
        if r_level == 0:
            return num_gen
        else:
            return num_gen * r_expected(num_gen - 1, r_level - 1)

    return r_expected(num_gen, r_level) + 1

# Math to determine how many messages each general expects to get total
def expected(n, m):
    sum = 0
    for i in range(1,m+1):
        sum += partial_factorial(n-2, i)
    return sum + 1

def partial_factorial(n, m):
    product = 1
    for i in range(0, m):
        product *= n - i
    return product


# Main
if len(sys.argv) < 4:
    print("Not enough arguments")
    exit()

gen_str = sys.argv[1]
gen_num = len(sys.argv[1])
order = sys.argv[2]
m = int(sys.argv[3])
expected = expected(gen_num, m)

# Create queues
queues = []
for i in range(0, gen_num):
    queues.append(queue.Queue())

# Create generals
generals = []
for i in range(0, len(gen_str)):
    generals.append(General(i, gen_str[i] == 'L', queues, expected))

# Start threads
for g in generals:
    g.start()

# Send initial message to commander to get the ball rolling
queues[0].put(Message(order, [], m+1))

# Wait for child threads to finish
for g in generals:
    g.join()
