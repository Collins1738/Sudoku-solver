'''
Sudoku solver

  This is a relatively fast sudoku solver (Leet Code Certified- Faster than 90% of all Leet Code Sudoku-solver submissions)

  It implements the regular backtracking method (trial and error) while also implementing a whole lot of actual human-like techniques in solving.

  The various human techniques it uses makes the program super-fast by minimalizing backtracking recursions.

  Backtracking in this program uses at most two folds of recursion (most other sudoku solvers use about 30-50 folds of backtracking making it extremely slow)

  I tested with this program, a Sudoku puzzle designed to defeat an average backtracking algorithm (sPuzzle4), and it didn't backtrack even once!

  Author: Collins Chikeluba


'''

class Solution:
    
  def solveSudoku(self, board):
    self.board=board
    self.changes=[]
    """
    Do not return anything, modify board in-place instead.
    """
    self.dictA={}
    self.startUpdate()
    self.toDel=[]
    self.almostSolve()
    if not self.solved():
      self.backTrack()
    return

  def displayBoard(self):
    print(self.board)
    return
      
  def backTrack(self):
    print("I backtracked")
    prevBoard=self.board.copy()
    prevDictA=self.dictA.copy()
    count=0
    while count<2:
      self.board=prevBoard.copy()
      self.dictA=prevDictA.copy()
      y=0
      while y<9:
        x=0
        breakAgain=False
        while x<9:
          if self.board[y][x]=="." and len(self.dictA[str(y)+str(x)][0])==2:
            self.board[y][x]=str(self.dictA[str(y)+str(x)][0][count])
            self.changes.append(str(y)+str(x))
            self.toDel.append(str(y)+str(x))
            breakAgain=True
            break;
          x+=1
        if breakAgain==True:
          break;
        y+=1
      self.delDict()
      self.update()
      self.almostSolve()
      
      if self.wrong():
        count+=1
        continue;
      if not self.solved():
        self.backTrack()
      return
    return
  
  def wrong(self):
    for y in range (0, 9):
      myArr=[]
      for x in range(0,9):
        if self.board[y][x]!=".":
          myArr.append(int(self.board[y][x]))
      for el in range(1, 10):
        if myArr.count(el)>1:
          return True
        
    for x in range(0,9):
      myArr=[]
      for y in range(0,9):
        if self.board[y][x]!=".":
          myArr.append(int(self.board[y][x]))
      for el in range(1, 10):
        if myArr.count(el)>1:
          return True
            
    for yOwn in range(0, 9, 3):
      for xOwn in range(0, 9, 3):
        yMin=yOwn
        xMin=xOwn
        yMax=yOwn+3
        xMax=xOwn+3
        myArr=[]
        for y in range(yMin, yMax):
          for x in range(xMin, xMax):
            if self.board[y][x]!=".":
              myArr.append(int(self.board[y][x]))
        for el in range(1, 10):
          if myArr.count(el)>1:
            return True
    return False
                          
  def checkOneOccurence(self):
    self.checkOneOccurenceRow()
    self.checkOneOccurenceColumn()
    self.checkOneOccurenceBox()
    return
      
  def almostSolve(self):
    count=0
    self.checkSingles()
    self.checkOneOccurence()
    while count<6: 
      self.checkSingleAlign() 
      self.addPairs()
      self.checkPairs()
      count+=1
    return
  
  def clearChanges(self):
    self.changes=[]
    return

  
  def solved(self):
    for y in range (0, 9):
      for x in range (0, 9):
        if self.board[y][x]==".":
          return False
    return True
  
  def removeRow(self, rowNum, element):
    element=int(element)
    for x in range(0, 9):
      if self.board[rowNum][x]=="." and element in self.dictA[str(rowNum)+str(x)][0]:
        self.dictA[str(rowNum)+str(x)][0].remove(element)
        if element in self.dictA[str(rowNum)+str(x)][1]:
          self.dictA[str(rowNum)+str(x)][1].remove(element)         
    return
  
  def removeCol(self, colNum, element):
    element=int(element)
    for y in range(0, 9):
      if self.board[y][colNum]=="." and element in self.dictA[str(y)+str(colNum)][0]:
        self.dictA[str(y)+str(colNum)][0].remove(element)
        if element in self.dictA[str(y)+str(colNum)][1]:
          self.dictA[str(y)+str(colNum)][1].remove(element)
    return
  
  def removeRowEx(self, rowNum, element):
    element=int(element)
    for x in range(0, 9):
      if self.board[rowNum][x]=="." and element in self.dictA[str(rowNum)+str(x)][0] and element not in self.dictA[str(rowNum)+str(x)][1]:
        self.dictA[str(rowNum)+str(x)][0].remove(element)              
    return
  
  def removeColEx(self, colNum, element):
    element=int(element)
    for y in range(0, 9):
      if self.board[y][colNum]=="." and element in self.dictA[str(y)+str(colNum)][0] and element not in self.dictA[str(y)+str(colNum)][1]:
        self.dictA[str(y)+str(colNum)][0].remove(element)
    return
  
  def removeBoxEx(self, y, x, element):
    element=int(element)
    array=self.makeList(self.boxOwner(y, x))
    y=array[0]
    x=array[1]
    yIn=y
    xIn=x
    yMax=y+3
    xMax=x+3
    for y in range (yIn, yMax):
      for x in range(xIn, xMax):
        if self.board[y][x]=="." and element in self.dictA[str(y)+str(x)][0] and element not in self.dictA[str(y)+str(x)][0]:
          self.dictA[str(y)+str(x)][0].remove(element)
    return
              
  def removeBox(self, y, x, element):
    element=int(element)
    array=self.makeList(self.boxOwner(y, x))
    y=array[0]
    x=array[1]
    yIn=y
    xIn=x
    yMax=y+3
    xMax=x+3
    for y in range (yIn, yMax):
      for x in range(xIn, xMax):
        if self.board[y][x]=="." and element in self.dictA[str(y)+str(x)][0]:
          self.dictA[str(y)+str(x)][0].remove(element)
          if element in self.dictA[str(y)+str(x)][1]:
            self.dictA[str(y)+str(x)][1].remove(element)
    return

  
  def update(self):
    for i in self.changes:
      y=int(i[0])
      x=int(i[1])
      self.removeRow(y, self.board[y][x])     
      self.removeCol(x, self.board[y][x])
      self.removeBox(y, x, self.board[y][x])
    self.changes=[]     
    return
  
      
  def singleInDict(self):
    for i in self.dictA.keys():
      if len(self.dictA[i][0])==1:
        return True
    return False
  
  def checkSingles(self):
    count=0
    while self.singleInDict(): 
      for i in self.dictA.keys():
        if len(self.dictA[i][0])==1:
          self.board[int(i[0])][int(i[1])]=str(self.dictA[i][0][0])
          self.changes.append(i)
          self.toDel.append(i)      
      self.delDict()
      self.update()
      count+=1
    return
  
  def addPairs(self):
    #check each row
                
    for y in range(0, 9): #for each row, ...
      myArr=[]
      for x in range(0, 9):
        if self.board[y][x]==".":
            myArr.extend(self.dictA[str(y)+str(x)][0]) #contains all posiblities totaled in row
      for i in range(1, 10):
        if myArr.count(i)==2:
          x=0
          while x<9: #find where that one occurence occured
            if self.board[y][x]=="." and (i in self.dictA[str(y)+str(x)][0]) and (i not in self.dictA[str(y)+str(x)][1]):
              self.dictA[str(y)+str(x)][1].append(i)
              self.dictA[str(y)+str(x)][1].sort()
            x+=1
                    
                    
    for x in range(0, 9): #for each column, ...
      myArr=[]
      for y in range(0, 9):
        if self.board[y][x]==".":
          myArr.extend(self.dictA[str(y)+str(x)][0]) #contains all posiblities totaled in column
      for i in range(1, 10):
        if myArr.count(i)==2:
            y=0
            while y<9: #find where that one occurence occured
                if self.board[y][x]=="." and (i in self.dictA[str(y)+str(x)][0]) and (i not in self.dictA[str(y)+str(x)][1]):
                    self.dictA[str(y)+str(x)][1].append(i)
                    self.dictA[str(y)+str(x)][1].sort()
                y+=1
                    
                    
    for y in range(0, 9, 3): 
      myArr=[]
      inY=y
      maxY=y+3
      for x in range(0, 9, 3):
        myArr=[]
        inX=x
        y=inY
        #for each box, ...
        maxX=x+3
        while y<maxY:
          x=inX
          while x<maxX:
            if self.board[y][x]==".":
              myArr.extend(self.dictA[str(y)+str(x)][0]) #contains all posiblities totaled in box
            x+=1
          y+=1
        for i in range(1, 10):
          if myArr.count(i)==2:
            y=inY
            x=inX
            while y<maxY:
              x=inX
              while x<maxX:
                if self.board[y][x]=="." and (i in self.dictA[str(y)+str(x)][0]) and (i not in self.dictA[str(y)+str(x)][1]):
                  self.dictA[str(y)+str(x)][1].append(i)
                  self.dictA[str(y)+str(x)][1].sort()
                x+=1
              y+=1
    return
  
  def makeString(self, array):
    string=""
    for i in array:
      string+=str(i)
    return string
  
  def makeList(self, string):
    array=[]
    for i in string:
      array.append(int(i))
    return array
  
  def checkSingleAlign(self):
    for y in range(0, 9, 3): 
      inY=y
      maxY=y+3
      for x in range(0, 9, 3):
        myArr=[]
        dictC={}
        inX=x
        #for each box, ...
        maxX=x+3
        for y in range(inY, maxY):
          for x in range(inX, maxX):
            if self.board[y][x]==".":
              for i in self.dictA[str(y)+str(x)][1]:
                if i in dictC.keys():
                  dictC[i]+=1
                else:
                  dictC[i]=1
        
        for i in dictC.keys():
          if dictC[i]>=2:
            dictX={}
            dictY={}
            # find them and check if same line
            for y in range(inY, maxY):
              for x in range(inX, maxX):
                if self.board[y][x]=="." and i in self.dictA[str(y)+str(x)][1]:
                  if x in dictX.keys():
                    dictX[x]+=1
                  else:
                    dictX[x]=1
                  if y in dictY.keys():
                    dictY[y]+=1
                  else:
                    dictY[y]=1
            for j in dictX.keys():
              if dictX[j]>=2:
                self.removeColEx(j, i)
            for j in dictY.keys():
              if dictY[j]>=2:
                self.removeRowEx(j, i)
      
  def getAllLists(self, list):
    array=[ [list[0], list[1]], [list[0], list[2]], [list[1], list[2]]  ]
    return array
      
  def checkPairs(self):
    for y in range(0, 9): 
      #for each row, ...
      myArr=[]
      dictB={}
      for x in range(0, 9):
        if self.board[y][x]==".":
          string=self.makeString(self.dictA[str(y)+str(x)][1])
          if len(string)==2 and string in dictB.keys():
            dictB[string]+=1
          elif len(string)>2:
            found=False
            for i in dictB.keys():
              if set(self.makeList(i)).issubset(set(self.makeList(string))):
                dictB[i]+=1
                found=True
            if not found:
              #put all possible lists in dictB
              allLists=self.getAllLists(self.makeList(string))
              for i in allLists:
                dictB[self.makeString(i)]=1
                      
          elif len(string)==2:
            dictB[string]=1
      for i in dictB.keys():
        if dictB[i]==2:
          # do all steps for pairs
          for x in range(0, 9):
            if self.board[y][x]=="." and set(self.makeList(i)).issubset(set(self.dictA[str(y)+str(x)][1])) :
              self.dictA[str(y)+str(x)][0]=self.makeList(i).copy()
              self.dictA[str(y)+str(x)][1]=self.makeList(i).copy()
            elif self.board[y][x]==".":
              for num in i:
                if int(num) in self.dictA[str(y)+str(x)][0]:
                  self.dictA[str(y)+str(x)][0].remove(int(num))
                    
        # print(dictB)
                    
                      
    for x in range(0, 9): #for each column, ...
      myArr=[]
      dictB={}
      for y in range(0, 9):
        if self.board[y][x]==".":
          string=self.makeString(self.dictA[str(y)+str(x)][1])
          if len(string)==2 and string in dictB.keys():
            dictB[string]+=1
          elif len(string)>2:
            found=False
            for i in dictB.keys():
              if set(self.makeList(i)).issubset(set(self.makeList(string))):
                dictB[i]+=1
                found=True
            if not found:
              #put all possible lists in dictB
              allLists=self.getAllLists(self.makeList(string))
              for i in allLists:
                dictB[self.makeString(i)]=1
                      
          elif len(string)==2:
            dictB[string]=1
      for i in dictB.keys():
        if dictB[i]==2:
          # do all steps for pairs
          for y in range(0, 9):
            if self.board[y][x]=="." and set(self.makeList(i)).issubset(set(self.dictA[str(y)+str(x)][1])) :
              self.dictA[str(y)+str(x)][0]=self.makeList(i).copy()
              self.dictA[str(y)+str(x)][1]=self.makeList(i).copy()
            elif self.board[y][x]==".":
              for num in i:
                if int(num) in self.dictA[str(y)+str(x)][0]:
                  self.dictA[str(y)+str(x)][0].remove(int(num))
      # print(dictB)
                      
      
    for y in range(0, 9, 3): 
      myArr=[]
      
      inY=y
      maxY=y+3
      for x in range(0, 9, 3):
        myArr=[]
        dictB={}
        inX=x
        #for each box, ...
        maxX=x+3
        for y in range(inY, maxY):
          for x in range(inX, maxX):
            if self.board[y][x]==".":
              string=self.makeString(self.dictA[str(y)+str(x)][1])
              if len(string)==2 and string in dictB.keys():
                dictB[string]+=1
              elif len(string)==2:
                dictB[string]=1
        for i in dictB.keys():
          if dictB[i]==2:
            # do all steps for pairs
            for y in range(inY, maxY):
              for x in range(inX, maxX):
                if self.board[y][x]=="." and i == self.makeString(self.dictA[str(y)+str(x)][1]):
                  self.dictA[str(y)+str(x)][0]=self.dictA[str(y)+str(x)][1].copy()
                elif self.board[y][x]==".":
                  for num in i:
                    if int(num) in self.dictA[str(y)+str(x)][0]:
                      self.dictA[str(y)+str(x)][0].remove(int(num))

    self.checkSingles()
    self.checkOneOccurenceRow()
    self.checkOneOccurenceColumn()
    self.checkOneOccurenceBox()
    return
      
  def checkOneOccurenceRow(self):
    #you have to check each box and each row
    #check each row
                
    for y in range(0, 9): #for each row, ...
      myArr=[]
      for x in range(0, 9):
        if self.board[y][x]==".":
          myArr.extend(self.dictA[str(y)+str(x)][0]) #contains all posiblities totaled in row
      for i in range(1, 10):
        if myArr.count(i)==1:
          x=0
          while x<9: #find where that one occurence occured
            if self.board[y][x]=="." and (i in self.dictA[str(y)+str(x)][0]):
              self.board[y][x]=str(i)
              self.changes.append(str(y)+str(x))
              self.toDel.append(str(y)+str(x))
              break
            x+=1 
    self.delDict()
    self.update()
    return
  
  def checkOneOccurenceColumn(self):
    #you have to check each box and each column
    #check each column
                
    for x in range(0, 9): #for each column, ...
      myArr=[]
      for y in range(0, 9):
        if self.board[y][x]==".":
            myArr.extend(self.dictA[str(y)+str(x)][0]) #contains all posiblities totaled in column
      for i in range(1, 10):
        if myArr.count(i)==1:
          y=0
          while y<9: #find where that one occurence occured
            if self.board[y][x]=="." and (i in self.dictA[str(y)+str(x)][0]):
              self.board[y][x]=str(i)
              self.changes.append(str(y)+str(x))
              self.toDel.append(str(y)+str(x))
              break
            y+=1
    self.delDict()
    self.update()
    return
  
  def checkOneOccurenceBox(self):
    #you have to check each box and each row
    #check each box
                
    for y in range(0, 9, 3): 
      myArr=[]
      inY=y
      maxY=y+3
      for x in range(0, 9, 3):
        myArr=[]
        inX=x
        y=inY
        #for each box, ...
        maxX=x+3
        while y<maxY:
          x=inX
          while x<maxX:
            if self.board[y][x]==".":
              myArr.extend(self.dictA[str(y)+str(x)][0]) #contains all posiblities totaled in box
            x+=1
          y+=1
        for i in range(1, 10):
          if myArr.count(i)==1:
            y=inY
            x=inX
            while y<maxY:
              x=inX
              breakAgain=False
              while x<maxX:
                if self.board[y][x]=="." and (i in self.dictA[str(y)+str(x)][0]):
                  self.board[y][x]=str(i)
                  self.toDel.append(str(y)+str(x))
                  self.changes.append(str(y)+str(x))
                  breakAgain=True
                  break
                x+=1
              if breakAgain:
                break
              y+=1
    self.delDict()
    self.update()
                      
    return
          
      
  def delDict(self):
    for i in self.toDel:
      del self.dictA[i]
    self.toDel=[]
    return
                  
      
  def startUpdate(self):
    y=0
    while y<9:
      x=0
      while x<9:
        if self.board[y][x]==".":
          self.dictA[str(y)+str(x)]=[[],[]]
          for i in range(1, 10):
            if (i not in self.box(y, x)) and (i not in self.row(y, x)) and (i not in self.column(y, x)):
              self.dictA[str(y)+str(x)][0].append(i) 
        x+=1
      y+=1
    return
  
  def boxOwner(self, y, x):
    if y in [0, 1, 2]:
      y=0
    elif y in [3, 4, 5]:
      y=3
    elif y in [6, 7, 8]:
      y=6
    if x in [0, 1, 2]:
      x=0
    elif x in [3, 4, 5]:
      x=3
    elif x in [6, 7, 8]:
      x=6
    return str(y)+str(x)
      
  
  def box(self, y, x):
    if y in [0, 1, 2]:
      y=0
    elif y in [3, 4, 5]:
      y=3
    elif y in [6, 7, 8]:
      y=6
    if x in [0, 1, 2]:
      x=0
    elif x in [3, 4, 5]:
      x=3
    elif x in [6, 7, 8]:
      x=6
    return self.iterateBox(y, x)
  
  def iterateBox(self, y, x):
    array=[]
    maxY=y+3
    maxX=x+3
    i=x
    while y<maxY:
      x=i
      while x<maxX:
        if self.board[y][x]!=".":
          array.append(int(self.board[y][x]))
        x+=1
      y+=1
    return array
          
  def row(self, y, x):
    array=[]
    for i in range(0, 9):
      if self.board[y][i]!=".":
        array.append(int(self.board[y][i]))
    return array
  
  def column(self, y, x):
    array=[]
    for i in range(0, 9):
      if self.board[i][x]!=".":
        array.append(int(self.board[i][x]))
    return array




sPuzzle1=[[".",".","9","7","4","8",".",".","."],["7",".",".",".",".",".",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],[".",".",".","8",".","3",".","2","."],[".",".",".",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]


# from youtube;
sPuzzle2=[[".","8",".",".","2",".","5","6","."],[".",".",".","1",".",".",".",".","7"],[".",".",".",".",".",".",".",".","."],[".","5",".",".","9",".","4",".","8"],[".",".","7","8",".",".",".",".","3"],[".","9",".",".","1",".",".","5","."],["2",".","4",".",".",".","8",".","."],[".","6",".",".","8","5",".",".","."],[".",".",".","2",".",".","1",".","."]]


#new hard
sPuzzle3=[[".",".",".",".",".","7",".",".","9"],[".","4",".",".","8","1","2",".","."],[".",".",".","9",".",".",".","1","."],[".",".","5","3",".",".",".","7","2"],["2","9","3",".",".",".",".","5","."],[".",".",".",".",".","5","3",".","."],["8",".",".",".","2","3",".",".","."],["7",".",".",".","5",".",".","4","."],["5","3","1",".","7",".",".",".","."]]

#Brute force hard 
sPuzzle4=[[".",".",".",".",".",".",".",".","."],[".",".",".",".",".","3",".","8","5"],[".",".","1",".","2",".",".",".","."],[".",".",".","5",".","7",".",".","."],[".",".","4",".",".",".","1",".","."],[".","9",".",".",".",".",".",".","."],["5",".",".",".",".",".",".","7","3"],[".",".","2",".","1",".",".",".","."],[".",".",".",".","4",".",".",".","9"]]


obj1=Solution()
obj1.solveSudoku(sPuzzle4)
obj1.displayBoard()
