
class LL1_Parser:

    def __init__(self):
        self.grammar = []
        self.terminals = []
        self.non_terminals = []
        self.first = dict()
        self.follow = dict()
        self.parsed_table = dict()
        self.read()
        self.find_first()
        self.find_follow()
        self.create_parsed_table()


    def read(self):
        #self.grammar = [['S','-','a','A','B','b'],['A','-','D','e'],['A','-','@',],['B','-','c'],['D','-','a'],['D','-','@']]
        #self.grammar = [['S','-','a','B','D','h'],['B','-','c','C'],['C','-','b','C'],['C','-','@'],['D','-','E','F'],['E','-','g'],['E','-','@'],['F','-','f'],['F','-','@']]
        #self.grammar = [['S','-','A'],['A','-','a','B','X'],['X','-','d'],['X','-','@'],['B','-','b']]
        #self.grammar = [['S','-','(','L',')'],['S','-','a'],['L','-','S','X'],['X','-',',','S','X'],['X','-','@']]
        #self.grammar = [['S','-','a','B','C','d'],['S','-','d','C','B','e'],['B','-','b','B'],['B','-','@'],['C','-','c','a'],['C','-','a','c'],['C','-','@']]
        self.grammar = [['S','-','a','A','b'],['S','-','a','B'],['A','-','a'],['A','-','c'],['B','-','b'],['B','-','@']]

        # comment the line above and uncomment the lines below to take command line input

        # print("Enter the number of production rules: ")
        # t = int(input())
        # for i in range(0,t):
        #     a = []
        #     print("Enter the production rule: ")
        #     stg = input()
        #     for j in range(0,len(stg)):
        #         a.append(stg[j])
        #     self.grammar.append(a)
        # print(self.grammar)

        for i in range(len(self.grammar)):
            for j in range(len(self.grammar[i])):
                if(self.grammar[i][j].isupper() and self.grammar[i][j] not in self.non_terminals):
                    self.non_terminals.append(self.grammar[i][j])

                if(self.grammar[i][j] not in self.non_terminals and self.grammar[i][j] not in ['-','@'] and self.grammar[i][j] not in self.terminals):
                    self.terminals.append(self.grammar[i][j])

        for i in range(len(self.grammar)):
            for j in range(len(self.grammar[i])):
                print(self.grammar[i][j],end='')
            print()

        print(self.terminals)
        print(self.non_terminals)


    def find_first(self):
        for i in range(len(self.non_terminals)):
            temp = set()
            self.first[self.non_terminals[i]] = self.firstt(self.non_terminals[i],temp,2)
        for i in range(len(self.terminals)):
            temp = set()
            temp.add(self.terminals[i])
            self.first[self.terminals[i]] = temp
        print("First: ", self.first)


    def find_follow(self):
        for k in self.non_terminals:
            temp = set()
            self.follow[k] = self.followw(k,temp)
        print("Follow : " , self.follow)


    def firstt(self,k,temp,l):
        for i in range(len(self.grammar)):

            if(k == self.grammar[i][0]):
                # if first token is a epsilon
                if(self.grammar[i][2] == '@' and len(self.grammar[i])-1 == 2):
                    temp.add(self.grammar[i][2])
                # if first token is a non_terminal
                elif(self.grammar[i][2] in self.non_terminals):
                        self.firstt(self.grammar[i][2],temp,l)
                        if ('@' in temp and len(self.grammar[i]) > 3):
                            self.firstt(self.grammar[i][l+1],temp,l+1)

                    # if first token in terminal
                else:
                    temp.add(self.grammar[i][2])
        return temp


    def followw(self,k,temp):
        if (self.grammar[0][0] == k):
            temp.add('$')
        for i in range(len(self.grammar)):
            if(k in self.grammar[i][2:len(self.grammar[i])]):
                j = self.grammar[i][:].index(k)
                if(j+1 <= len(self.grammar[i])-1):
                    if(self.grammar[i][j+1] in self.first):
                        if('@' not in self.first[self.grammar[i][j+1]]):
                            t = (self.first[self.grammar[i][j+1]])
                            for item in t:
                                temp.add(item)
                        else:
                            n = j+1
                            flag = 0
                            while(n <= len(self.grammar[i])-1):
                                t = self.first[self.grammar[i][n]]
                                if('@' in self.first[self.grammar[i][n]]):
                                    t.remove('@')
                                    for item in t:
                                        temp.add(item)
                                else:
                                    for item in t:
                                        temp.add(item)
                                    flag = 1
                                    break
                                n = n+1
                            if(flag == 0 and self.grammar[i][0] != self.grammar[i][n-1] and self.grammar[i][n-1] in self.non_terminals):
                                self.followw(self.grammar[i][0],temp)
                            else:
                                t = self.first[self.grammar[i][n-1]]
                                for item in t:
                                    temp.add(item)

                elif(len(self.grammar[i])-1 == j+1 and self.grammar[i][0] != self.grammar[i][j+1]):      # Non-Term. last char in rule
                    t = self.first[self.grammar[i][j+1]]
                    if('@' in t):
                        t.remove('@')
                        for item in t:
                            temp.add(item)
                        self.followw(self.grammar[i][0],temp)
                    else:
                        for item in t:
                            temp.add(item)
                else:
                    if(len(self.follow[self.grammar[i][0]])):
                        t = self.follow[self.grammar[i][0]]
                        for item in t:
                            temp.add(item)
                    else:
                        self.followw(self.grammar[i][0],temp)


        return temp

    def create_parsed_table(self):
        # initialising
        head = self.terminals
        head.insert(len(self.terminals),'$')
        self.parsed_table['NT/T'] = head
        alert = 0

#         adding values to the table
        for i in self.non_terminals:
            final_list = dict()
            final = list()
            for rule in range(len(self.grammar)):
                if i == self.grammar[rule][0]:
                    if('@' not in self.grammar[rule]):     #table filling using first
                        t = self.first[self.grammar[rule][0]]
                        for item in t:
                            if(self.grammar[rule][2] == item):
                                if(head.index(item) in final_list):
                                    alert = 1
                                else:
                                    final_list[head.index(item)] = self.grammar[rule]

                            else:
                                t_nt = self.first[self.grammar[rule][2]]  #else find FIRST(non terminal)
                                if('@' in t_nt):
                                    t_nt.remove('@')
                                if(item in t_nt):
                                    if(head.index(item) in final_list):
                                        alert = 1
                                    else:
                                        final_list[head.index(item)] = self.grammar[rule]
                    else: #when we have '@' production rule
                        t_fol = self.follow[self.grammar[rule][0]]
                        for item in t_fol:
                            if(head.index(item) in final_list):
                                    alert = 1
                            else:
                                final_list[head.index(item)] = self.grammar[rule]
            for fl in range(0,len(head)):
                if(fl in final_list):
                    final.append(final_list[fl])
                else:
                    final.append('0')
            self.parsed_table[i] = final
        if(alert == 1):
            print("More than one entry for a given cell. Not LL1 grammar")
        else:
            print()
            print("LL(1) parser table: \n")
            for i in self.parsed_table:
                print(i,"\t",self.parsed_table[i])



if __name__ == "__main__":

    LL1parse = LL1_Parser()
