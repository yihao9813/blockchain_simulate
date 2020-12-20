# ������������Ӧ��-������ҵ����

������YI HAO CHING

ѧ�ţ�517030990016

ѧԺ��������Ϣ���������ѧԺ

## ���ݽṹ����
### ����
```
class Block:
    #���ڱ�������Ϣ��ǰ����ϣֵ�͵�ǰ��ϣֵ
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
### ��������
```
class blockchain:
    #��ʼ����ͷ�ͼ�¼���ĳ���
    def __init__(self):
        self.head = Block(None,None)
        self.length = 0
    #��ӡ�����������п����Ϣ
    def display(self):
        elements = []
        current_block = self.head
        while current_block.tail != None:
            current_block = current_block.tail
            print("Node:",current_block.index,"Transaction:",current_block.transaction,"\nPrevious Hash:",current_block.pre_hash,"\nCurrent Hash:",current_block.current_hash,"\n")
            #elements.append((current_block.index,current_block.transaction,current_block.timestamp,current_block.current_hash))
        return elements
    #����µĿ���������
    def add(self,new_block):
        current_block = self.head
        #����β������ӽ�ȥ��
        while current_block.tail != None:
            current_block = current_block.tail
        #����һ����Ĺ�ϣֵ�͵�ǰ������ݺϲ�����ϣ��������
        tmp = str(new_block.index) + str(new_block.transaction) + str(new_block.timestamp) + str(current_block.current_hash)
        tmp = sha256(tmp.encode()).hexdigest()
        new_block.current_hash = tmp
        new_block.pre_hash = current_block.current_hash
        new_block.index = self.length
        current_block.tail = new_block
        new_block.head = current_block 
        self.length += 1
```
## ��Ҫ��������
### ���ɿ麯��
```
def generateBlock(prob):
    #���ݸ������ɿ�
    #�����ɳɹ��������µĿ飬��ʧ���򷵻�None
    if random.uniform(0,1) < prob:
        new_block = Block(random.uniform(0,10),datetime.now())
        return new_block
    return None
```
### �ڿ���
```
def mining(Node,prob):
    #ѭ��һ��ģ��ÿ���ڵ㶼�����ڿ�һ��
    for i in range(len(Node)):
        new_block = generateBlock(prob)
        #�ɹ�����������ӽ��ڵ�����鱣�棬���㲥
        if new_block != None:
            Node[i].append(new_block)
```
### �㲥����
```
def broadcast(block_head,Node,evil_node):
    #����Ƕ���ڵ��򲻽��й�ʶ�������ڿ�
    for i in range(len(Node)):
        if i not in evil_node:  #����ڵ㲻�Ƕ���ڵ�
            for j in range(len(Node[i])):
                block_head.add(Node[i][j])
            Node[i] = []
```
### �жϷֲ湥���ɹ������
```
def isSuccess(block_head,evil_blocks,Node,evil_node):
    #����ÿ������ڵ㣬������ڵ��ĳ����Ƿ�������
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
### �ֲ湥������
```
def attack(node_num,prob,evil_node_percentage): 
    #ģ��100���ڵ�ͳ�ʼ��
    Node = [[] for j in range(node_num)]
    block_head = blockchain()   #blockchain head
    evil_blocks = []
    #������ڵ�������ѡȡ������Ϊ����ڵ�
    evil_node = [random.randint(0,len(Node)-1) for _ in range(int(node_num*evil_node_percentage)) ]

    for i in range(1000):
        mining(Node,prob)
        broadcast(block_head,Node,evil_node)
        #�жϷֲ湥���Ƿ�ɹ�
        flag = isSuccess(block_head,evil_blocks,Node,evil_node)
        if flag is True:    #���ɹ�
            #print("Round: %d ,Attack success!"%(i))
            return True
    #��������������������
    speed = block_head.length/1000
    #print("�������� = %f"%(speed))
    
    #print(block_head.display())    #��ʾ�����������еĿ�����ݺ͹�ϣֵ
    #print("Round = %d, Current block length = %d , evil blocks total = %d\n"%(i,block_head.length,len(evil_blocks)))
    return False
```
### ��ʵ�ڵ�Ͷ���ڵ����㺯��
```
#����ʵ�ڵ������
def calcHonestblock(Node,evil_node):
    total = 0
    for i in range(len(Node)):
        if i not in evil_node:  #����ǳ�ʵ�ڵ�
            total += len(Node[i])
    return total

#������ڵ������
def calcEvilblock(Node,evil_node):
    total = 0
    for i in evil_node:     #����Ƕ���ڵ�
        total += len(Node[i])
    return total
```
### ��˽�ڿ�Ĺ㲥���Ժ���
����ڵ���ݲ��Ծ���Ҫ��Ҫ�㲥��
```
def selfish_broadcast(block_head,Node,evil_node):
    honest_blocks_number = calcHonestblock(Node,evil_node)
    evil_blocks_number = calcEvilblock(Node,evil_node)
    #print(honest_blocks_number,evil_blocks_number)
    #���1:�����ʵ�ڵ����࣬�����ڵ㲻�㲥�����ڿ󣬳�ʵ�ڵ�㲥
    if evil_blocks_number < honest_blocks_number:   
        for i in range(len(Node)):
            if i not in evil_node:   #����ǳ�ʵ�ڵ�
                for j in range(len(Node[i])):
                   block_head.add(Node[i][j])    #���������
                Node[i] = []
        return 0
    #���2���������ڵ�Ŀ�ֻ�����ȳ�ʵ�ڵ�1�飬Ȼ���ʵ�ڵ��ڳ�һ���¿飨��������ͬ���������ڵ�ͳ�ʵ�ڵ㾺���㲥
    elif evil_blocks_number == honest_blocks_number:
        if random.uniform(0,1) < 0.5:   #�Ը������ѡȡ
            #�����㲥
            for i in range(len(Node)):
                if i in evil_node:      #����Ƕ���ڵ�
                    for j in range(len(Node[i])):
                        block_head.add(Node[i][j])
                    Node[i] = []
                else:   #��ʵ�ڵ㾺��ʧ�ܣ�����
                    Node[i] = []
            return evil_blocks_number
        else:
            #��ʵ�ڵ�㲥
            for i in range(len(Node)):
                if i not in evil_node:  #��ʵ�ڵ�
                    for j in range(len(Node[i])):
                        block_head.add(Node[i][j])
                    Node[i] = []
                else:   #����ڵ㾺��ʧ�ܣ�����
                    Node[i] = []
            return 0
    #���3���������ڵ�Ŀ�ȳ�ʵ�ڵ��2�飬Ȼ���ʵ�ڵ��ڳ��¿飨��������1�飩�����ڵ㣬�����ڵ�㲥�飬��ʵ�ڵ�Ŀ鱻����
    elif evil_blocks_number == honest_blocks_number + 1:
        for i in range(len(Node)):
            if i in evil_node:      #����Ƕ���ڵ�
                for j in range(len(Node[i])):
                    block_head.add(Node[i][j])
                Node[i] = []
            else:   #��ʵ�ڵ�鱻����
                Node[i] = []
        return evil_blocks_number
    #���4���������ڵ�Ŀ�ȳ�ʵ�ڵ��>2�飬Ȼ���ʵ�ڵ��ڳ��¿飬����ڵ�ֱ�ӹ㲥һ���飬ʣ�������
    else:
        number = 0
        for i in range(len(Node)):
            if i in evil_node:      #����Ƕ���ڵ�
                for j in range(len(Node[i])):
                    if number <= honest_blocks_number + 1:
                        block_head.add(Node[i][0])
                        number += 1
                        Node[i].remove(Node[i][0])  #�ӽ����ɾ��
            else:   #��ʵ�ڵ�鱻����
                Node[i] = []
        return number
```
## ����
�����У��Ҳ�û����ǰ����һ�������������������г�ʵ�ڵ�Ͷ���ڵ㶼�Ǵ��㿪ʼ�����

һ��ִ��attack()������selfish_mining()����Ϊ��ʵ�����ڵ㾭����1000�ε��ڿ�
### �ֲ湥������
��������main()���ֱ�ʹ�ò�ͬ�Ĳ�������attack()����������һ�ٴη���
```
success = 0     #��¼�ֲ湥���ɹ�����
for _ in range(100):
    if attack(node_num,prob,evil_node):
        success += 1
print("�ڵ�����%d\t������ʣ�%f\t����ڵ������%f\t�����ɹ�������%d"%(node_num,prob,evil_node_percentage,success))
```
#### ���Խ��
�̶��������ڵ���100���������0.0005

��û�ж���ڵ���ڵ�����£�����������������Ϊ0.0495�����趨�ĳ������/100���ڵ�ǳ�����

�������ҷֱ���ÿ����������100�εķֲ湥�����棬����������10�֣���ȡ�����ƽ��ֵ���±�
| ����ڵ���� | 1000���ڿ��зֲ湥���ɹ���ƽ������ |
| :-----------: | :-----------: |
| 10% | 2.6 |
| 20% | 9.7 |
| 30% | 32.5 |
| 40% | 56.7 |

������ڵ�Ϊ10%���ֲ湥���ɹ�ʱ���ĳ���ͨ��������һ��ʼ��ͬ�������ʱ�򣬼�����=1ʱ�������ʱ��û�����ɹ���֮�󼸺�����ɹ���

������ڵ�Ϊ20%ʱ���ֲ湥���ɹ�ʱ��������ɴﵽ6

������ڵ�Ϊ30%ʱ���ֲ湥���ɹ�ʱ��������ɴﵽ14

������ڵ�Ϊ40%ʱ���ֲ湥���ɹ�ʱ��������ɴﵽ20


### ��˽�ڿ����
����main()�����н���100�εĺ������ã�selfish_mining�����У���ʵ�ڵ�Ͷ���ڵ���ѭ�����������ڿ󣬳�ʵ�ڵ��ڵ����ֱ�Ӵ��㹫����������ڵ���ݹ������Խ��й���

```
profit = 0
for _ in range(100):
    tmp = selfish_mining(node_num,prob,evil_node)
    profit += tmp
print(profit/100)
```
#### ���Խ��
�������Լ��㣬�ҵõ�����˽�ڿ������ǳ����ȶ�����͵�������0.6477�������2.5���ձ������0.8-1.25֮�䡣���������Ϊ���趨����˽�ڿ󹫲����Բ��������µġ�




