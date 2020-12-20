from hashlib import sha256
import random
import time
import threading
from datetime import datetime

class Block:
    def __init__(self,transaction,timestamp):
        self.index = None
        self.transaction = transaction
        self.timestamp = timestamp
        self.pre_hash = None
        self.current_hash = None
        self.head = None
        self.tail = None
    
    def getpreHash(self):
        return self.pre_hash

    def getcurrentHash(self):
        return self.current_hash

class blockchain:
    def __init__(self):
        self.head = Block(None,None)
        self.length = 0

    def display(self):
        elements = []
        current_block = self.head
        while current_block.tail != None:
            current_block = current_block.tail
            print("Node:",current_block.index,"Transaction:",current_block.transaction,"\nPrevious Hash:",current_block.pre_hash,"\nCurrent Hash:",current_block.current_hash,"\n")
            #elements.append((current_block.index,current_block.transaction,current_block.timestamp,current_block.current_hash))
        return elements

    def add(self,new_block):
        #new_node
        current_block = self.head
        #找链尾，并添加进去链
        while current_block.tail != None:
            current_block = current_block.tail
        #用上一个块的哈希值和当前块的数据合并作哈希，并保存
        tmp = str(new_block.index) + str(new_block.transaction) + str(new_block.timestamp) + str(current_block.current_hash)
        tmp = sha256(tmp.encode()).hexdigest()
        new_block.current_hash = tmp
        new_block.pre_hash = current_block.current_hash
        new_block.index = self.length
        current_block.tail = new_block
        new_block.head = current_block 
        self.length += 1   

def generateBlock(prob):
    #根据概率生成块
    if random.uniform(0,1) < prob:
        new_block = Block(random.uniform(0,10),datetime.now())
        return new_block
    return None

def mining(Node,prob):
    #循环一轮模拟每个节点都尝试挖矿一次
    for i in range(len(Node)):
        new_block = generateBlock(prob)
        #成功生产
        if new_block != None:
            Node[i].append(new_block)

def broadcast(block_head,Node,evil_node):
    #如果是恶意节点则不进行共识，继续挖矿
    for i in range(len(Node)):
        if i not in evil_node:  #如果节点不是恶意节点
            for j in range(len(Node[i])):
                block_head.add(Node[i][j])
            Node[i] = []


def isSuccess(block_head,evil_blocks,Node,evil_node):
    #遍历每个恶意节点，检查恶意节点块的长度是否大于最长链
    if block_head.length == 0:
        return False
    for i in evil_node:
        for j in Node[i]:
            evil_blocks.append(j)
        Node[i]= []
        if len(evil_blocks) > block_head.length:
            return True
    return False

#分叉攻击仿真
def attack(node_num,prob,evil_node): 
    #模拟100个节点和初始化
    Node = [[] for j in range(node_num)]
    block_head = blockchain()   #blockchain head
    evil_blocks = []
    
    for i in range(1000):
        mining(Node,prob)
        broadcast(block_head,Node,evil_node)
        #判断分叉攻击是否成功
        flag = isSuccess(block_head,evil_blocks,Node,evil_node)
        if flag is True:    #若成功
            #print("Round: %d ,Attack success!"%(i))
            #print("Round = %d, Current blockchain length = %d , evil blocks total = %d\n"%(i,block_head.length,len(evil_blocks)))
            return True
    #计算区块链的增长速率
    speed = block_head.length/1000
    #print("链增长速率 = %f(块/轮)"%(speed))
    
    #print(block_head.display())    #显示区块链上所有的块的数据和哈希值
    return False

#检查诚实节点块总数
def calcHonestblock(Node,evil_node):
    total = 0
    for i in range(len(Node)):
        if i not in evil_node:  #如果是诚实节点
            total += len(Node[i])
    return total

#检查恶意节点块总数
def calcEvilblock(Node,evil_node):
    total = 0
    for i in evil_node:
        total += len(Node[i])
    return total

def selfish_broadcast(block_head,Node,evil_node):
    honest_blocks_number = calcHonestblock(Node,evil_node)
    evil_blocks_number = calcEvilblock(Node,evil_node)
    #print(honest_blocks_number,evil_blocks_number)
    #情况1:如果诚实节点块更多，则恶意节点不广播继续挖矿，诚实节点广播
    if evil_blocks_number < honest_blocks_number:   
        for i in range(len(Node)):
            if i not in evil_node:   #如果是诚实节点
                for j in range(len(Node[i])):
                   block_head.add(Node[i][j])    #将块加入链
                Node[i] = []
        return 0
    #情况2：如果恶意节点的块只比领先诚实节点1块，然后诚实节点挖出一个新块（即块数相同），则恶意节点和诚实节点竞争广播
    elif evil_blocks_number == honest_blocks_number:
        if random.uniform(0,1) < 0.5:   #以概率随机选取
            #恶意块广播
            for i in range(len(Node)):
                if i in evil_node:      #如果是恶意节点
                    for j in range(len(Node[i])):
                        block_head.add(Node[i][j])
                    Node[i] = []
                else:   #诚实节点竞争失败，丢弃
                    Node[i] = []
            return evil_blocks_number
        else:
            #诚实节点广播
            for i in range(len(Node)):
                if i not in evil_node:  #诚实节点
                    for j in range(len(Node[i])):
                        block_head.add(Node[i][j])
                    Node[i] = []
                else:   #恶意节点竞争失败，丢弃
                    Node[i] = []
            return 0
    #情况3：如果恶意节点的块比诚实节点多2块，然后诚实节点挖出新块（即恶意块多1块）则恶意节点，则恶意节点广播块，诚实节点的块被丢弃
    elif evil_blocks_number == honest_blocks_number + 1:
        for i in range(len(Node)):
            if i in evil_node:      #如果是恶意节点
                for j in range(len(Node[i])):
                    block_head.add(Node[i][j])
                Node[i] = []
            else:   #诚实节点块被丢弃
                Node[i] = []
        return evil_blocks_number
    #情况4：如果恶意节点的块比诚实节点多>2块，然后诚实节点挖出新块，恶意节点直接广播一个块，剩余的留着
    else:
        number = 0
        for i in range(len(Node)):
            if i in evil_node:      #如果是恶意节点
                for j in range(len(Node[i])):
                    if number <= honest_blocks_number + 1:
                        block_head.add(Node[i][0])
                        number += 1
                        Node[i].remove(Node[i][0])  #加进块后删除
            else:   #诚实节点块被丢弃
                Node[i] = []
        return number

def selfish_mining(node_num,prob,evil_node):
    #模拟100个节点和初始化
    Node = [[] for j in range(node_num)]
    block_head = blockchain()   #blockchain head
    #按恶意节点比例随机选取数字作为恶意节点  
    number = 0
    for _ in range(1000):
        mining(Node,prob)
        number += selfish_broadcast(block_head,Node,evil_node)
    #返回 自私挖矿的块在链中的比例/恶意节点的比例
    return ((number/block_head.length)/(len(evil_node)/node_num))

def main():
    #把代码的第106行的注释符去掉可以打印区块链增长的速率
    node_num = 100      #节点数
    prob = 0.0005       #出块的概率
    evil_node_percentage = 0.1  #恶意节点的比例
    evil_node = []
    #按恶意节点比例随机选取数字作为恶意节点
    while len(evil_node) < int(node_num*evil_node_percentage):
        tmp = random.randint(0,node_num-1)
        if tmp not in evil_node:
            evil_node.append(tmp)
    
    #分叉攻击仿真
    success = 0     #记录分叉攻击成功次数
    for _ in range(100):
         if attack(node_num,prob,evil_node):
             success += 1
    print("节点数：%d\t出块概率：%f\t恶意节点比例：%f\t攻击成功次数：%d"%(node_num,prob,evil_node_percentage,success))
    
    
    #自私挖矿仿真
    profit = 0
    for _ in range(100):
        tmp = selfish_mining(node_num,prob,evil_node)
        profit += tmp
    print(profit/100)
    #return success


main()
'''
#运行10轮计算成功次数平均值
total = 0
for _ in range(10):
    total += main()
print(total/10)
'''