# 区块链技术与应用-期中作业报告

姓名：YI HAO CHING

学号：517030990016

学院：电子信息与电气工程学院

## 数据结构介绍
### 块类
```
class Block:
    #用于保存块的信息，前链哈希值和当前哈希值
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
```
### 区块链类
```
class blockchain:
    #初始化链头和记录链的长度
    def __init__(self):
        self.head = Block(None,None)
        self.length = 0
    #打印区块链上所有块的信息
    def display(self):
        elements = []
        current_block = self.head
        while current_block.tail != None:
            current_block = current_block.tail
            print("Node:",current_block.index,"Transaction:",current_block.transaction,"\nPrevious Hash:",current_block.pre_hash,"\nCurrent Hash:",current_block.current_hash,"\n")
            #elements.append((current_block.index,current_block.transaction,current_block.timestamp,current_block.current_hash))
        return elements
    #添加新的块入区块链
    def add(self,new_block):
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
```
## 重要函数介绍
### 生成块函数
```
def generateBlock(prob):
    #根据概率生成块
    #若生成成功，返回新的块，若失败则返回None
    if random.uniform(0,1) < prob:
        new_block = Block(random.uniform(0,10),datetime.now())
        return new_block
    return None
```
### 挖矿函数
```
def mining(Node,prob):
    #循环一轮模拟每个节点都尝试挖矿一次
    for i in range(len(Node)):
        new_block = generateBlock(prob)
        #成功生产，则添加进节点的数组保存，待广播
        if new_block != None:
            Node[i].append(new_block)
```
### 广播函数
```
def broadcast(block_head,Node,evil_node):
    #如果是恶意节点则不进行共识，继续挖矿
    for i in range(len(Node)):
        if i not in evil_node:  #如果节点不是恶意节点
            for j in range(len(Node[i])):
                block_head.add(Node[i][j])
            Node[i] = []
```
### 判断分叉攻击成功与否函数
```
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
```
### 分叉攻击仿真
```
def attack(node_num,prob,evil_node_percentage): 
    #模拟100个节点和初始化
    Node = [[] for j in range(node_num)]
    block_head = blockchain()   #blockchain head
    evil_blocks = []
    #按恶意节点比例随机选取数字作为恶意节点
    evil_node = [random.randint(0,len(Node)-1) for _ in range(int(node_num*evil_node_percentage)) ]

    for i in range(1000):
        mining(Node,prob)
        broadcast(block_head,Node,evil_node)
        #判断分叉攻击是否成功
        flag = isSuccess(block_head,evil_blocks,Node,evil_node)
        if flag is True:    #若成功
            #print("Round: %d ,Attack success!"%(i))
            return True
    #计算区块链的增长速率
    speed = block_head.length/1000
    #print("出块速率 = %f"%(speed))
    
    #print(block_head.display())    #显示区块链上所有的块的数据和哈希值
    #print("Round = %d, Current block length = %d , evil blocks total = %d\n"%(i,block_head.length,len(evil_blocks)))
    return False
```
### 诚实节点和恶意节点块计算函数
```
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
    for i in evil_node:     #如果是恶意节点
        total += len(Node[i])
    return total
```
### 自私挖矿的广播策略函数
恶意节点根据策略决定要不要广播块
```
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
```
## 测试
测试中，我并没有提前生成一条区块链，而是让所有诚实节点和恶意节点都是从零开始组成链

一次执行attack()函数或selfish_mining()函数为诚实与恶意节点经过了1000次的挖矿
### 分叉攻击测试
在主函数main()，分别使用不同的参数调用attack()函数，进行一百次仿真
```
success = 0     #记录分叉攻击成功次数
for _ in range(100):
    if attack(node_num,prob,evil_node):
        success += 1
print("节点数：%d\t出块概率：%f\t恶意节点比例：%f\t攻击成功次数：%d"%(node_num,prob,evil_node_percentage,success))
```
#### 测试结果
固定参数：节点数100，出块概率0.0005

在没有恶意节点存在的情况下，区块链的增长速率为0.0495，与设定的出块概率/100个节点非常近似

在这里我分别用每个参数进行100次的分叉攻击仿真，并且运行了10轮，再取结果的平均值作下表
| 恶意节点比例 | 1000次挖矿中分叉攻击成功的平均次数 |
| :-----------: | :-----------: |
| 10% | 2.6 |
| 20% | 9.7 |
| 30% | 32.5 |
| 40% | 56.7 |

当恶意节点为10%，分叉攻击成功时链的长度通常都是在一开始共同组成链的时候，即链长=1时。如果这时候没攻击成功，之后几乎不会成功了

当恶意节点为20%时，分叉攻击成功时最长的链长可达到6

当恶意节点为30%时，分叉攻击成功时最长的链长可达到14

当恶意节点为40%时，分叉攻击成功时最长的链长可达到20


### 自私挖矿测试
我在main()函数中进行100次的函数调用，selfish_mining函数中，诚实节点和恶意节点在循环体里轮流挖矿，诚实节点挖到块后直接打算公布，而恶意节点根据公布策略进行公布

```
profit = 0
for _ in range(100):
    tmp = selfish_mining(node_num,prob,evil_node)
    profit += tmp
print(profit/100)
```
#### 测试结果
经过测试计算，我得到的自私挖矿的收益非常不稳定，最低的收益有0.6477，最高有2.5，普遍会落在0.8-1.25之间。这可能是因为我设定的自私挖矿公布策略不好所导致的。




