import time
def pushheap(l, elem):
    l.append(elem)
    down(l, 0, len(l)-1)

def popheap(l):
    elem = l.pop()    
    if l:
        last = l[0]
        l[0] = elem
        up(l, 0)
        return last
    return elem

def down(l, src, pos):
    last = l[pos]
    while pos > src:
        posparent = (pos - 1) >> 1
        parent = l[posparent]
        if last < parent:
            l[pos] = parent
            pos = posparent
            continue
        break
    l[pos] = last

def up(l, pos):
  
    last = l[pos]
    src = pos
    endpos = len(l)    
    poschild = 1+(pos*2)    
    while poschild < endpos:
        
        rightpos = 1+poschild 
        if rightpos < endpos and not l[poschild] < l[rightpos]:
            childpos = rightpos
        
        l[pos] = l[poschild]
        pos = poschild
        poschild = 1+(pos*2)
    
    l[pos] = last
    down(l, src, pos)

def check_valid_func(src,W,H,dp,zelev):
	x=src[0]
	y=src[1]
	neighbors=[(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
	neighbors_list=[]
	for neighbor in neighbors:
		if neighbor[0]<0 or neighbor[0]>H or neighbor[1]<0 or neighbor[1]>W:
			continue
		elif abs(dp[neighbor[0]][neighbor[1]]-dp[src[0]][src[1]])>zelev:
			continue
		else:
			temp=neighbors[0]
			neighbors[0]=neighbors[1]
			neighbors[1]=temp
			neighbors_list.append(neighbor)
	return neighbors_list		

def compare(s1,s2):
	if s1==s2:
		return True
	else:
		return False	

def bfsfun(dp,zelev,W,H,src,dest):	
	
	l1=[src]
	visqueue=set()
	while l1:
		if l1[0]==src:
			path=[l1.pop(0)]
		else:
			path=l1.pop(0)
		top_element=path[-1]
		print(top_element)
		if top_element==dest:
			return path
		elif top_element in visqueue:
			continue
		else:
			
			for neighbor in check_valid_func(top_element,W,H,dp,zelev):
				if neighbor in visqueue:
					continue
				else:
				
					path_new=list(path)
					path_new.append(neighbor)
					l1.append(path_new)
					#print(path_new)
			visqueue.add(top_element)
	return None

def getcost(src,dest):
	cost=0
	x,y=src
	x1,y1=dest
	xdiff=abs(x-x1)
	ydiff=abs(y-y1)
	if xdiff==1 and ydiff==1:
		cost=14
	else:
		cost=10
	return cost
	
def ucsfun(src,dest,W,H,dp,zelev):
	visited={}
	l1=tuple([0,src,[]])
	l3=[]
	l3.append(l1)
	while len(l3)>0:
		current_cost,current,path=popheap(l3)
		if current in visited.keys():
			if visited[current]<current_cost:
				continue
		path=path+[current]
		if current==dest:
			return path
		visited[current]=current_cost	
		for neighbor in getneighbors1(current,W,H,dp,zelev,visited):
			neighborcost=getcost(neighbor,current)
			total_cost=neighborcost+current_cost
			pushheap(l3,(total_cost,neighbor,path))
	return None

def heuristicfunc1(neighbor,dest):
	x_diff=abs(neighbor[0]-dest[0])
	y_diff=abs(neighbor[1]-dest[1])
	#h=max(x_diff,y_diff)
	#return h
	return((x_diff+y_diff)+(-1*min(x_diff,y_diff)))

def getneighbors1(src,W,H,dp,zelev,visited):
	x=src[0]
	y=src[1]
	neighbors=[(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
	neighbors_list=[]
	
	for neighbor in neighbors:
		if neighbor[0]<0 or neighbor[0]>H or neighbor[1]<0 or neighbor[1]>W:
			continue
		elif abs(dp[neighbor[0]][neighbor[1]]-dp[src[0]][src[1]])>zelev:
			continue
		elif neighbor in visited:
			continue	
		else:
			temp=neighbors[0]
			neighbors[0]=neighbors[1]
			neighbors[1]=temp
			neighbors_list.append(neighbor)
			
	return neighbors_list	

def getcost1(dp,src,dest,zelev):
	cost=0
	x,y=src
	x1,y1=dest
	xdiff=abs(x-x1)
	ydiff=abs(y-y1)
	zelevcost=abs(dp[src[0]][src[1]]-dp[dest[0]][dest[1]])
	if xdiff==1 and ydiff==1:
		cost=14
	else:
		cost=10
	return (cost+zelevcost)
	
def astarfun(src,dest,W,H,dp,zelev):
	visited={}
	l1=tuple([0,src,[]])
	l2=[]
	l2.append(l1)
	while len(l2)>0:
		current_cost,current,path=popheap(l2)
		print(path)
		if current in visited.keys():
			if visited[current]<current_cost:
				continue
		path=path+[current]
		if current==dest:
			return path
		visited[current]=current_cost	
		for neighbor in getneighbors1(current,W,H,dp,zelev,visited):
			neighborcost=getcost1(dp,neighbor,current,zelev)+heuristicfunc1(neighbor,dest)
			total_cost=neighborcost+current_cost
			pushheap(l2,(total_cost,neighbor,path))
	return None	


def main():
	'''
	W,H,X,Y,zelev,N=0,0,0,0,0,0
	landingsite1,landingsite2=0,0
	dest1,dest2=0,0
	'''
	with open('input.txt','r+') as f:
		algo=f.readline().strip()
		W,H=[int(x) for x in next(f).split()]
		X,Y=[int(y) for y in next(f).split()]
		zelev=int(f.readline(3))
		N=int(f.readline(4))
		targetx=[None]*N
		targety=[None]*N
		for i in range(N):
			targetx[i],targety[i]=[int(x) for x in next(f).split()]
		dp=[]
		for i in range(0,H):
			dp.append(list(map(int,f.readline().split()[:W])))
		f.close()
	
	with open('output.txt','w+') as f1:	
		if algo=="BFS":
			src=(Y,X)
			
			for i in range(N):
				dest1,dest2=targetx[i],targety[i]
				dest=(dest2,dest1)
				ans_path=bfsfun(dp,zelev,W-1,H-1,src,dest)
				 
				if i==(N-1):
					if ans_path==None:
						f1.write('FAIL')
					else:
						f1.write(' '.join([str(i[1]) + "," + str(i[0]) for i in ans_path]))
				else:
					if ans_path==None:
						f1.write('FAIL'+"\n")
					else:
						f1.write(' '.join([str(i[1]) + "," + str(i[0]) for i in ans_path])+"\n")
							
							
				
		elif algo=="UCS":
			src=(Y,X)
			for i in range(N):
				dest1,dest2=targetx[i],targety[i]
				dest=(dest2,dest1)
				ans_path=ucsfun(src,dest,W-1,H-1,dp,zelev)		
				if i==(N-1):
					if ans_path==None:
						f1.write('FAIL')
					else:
						f1.write(' '.join([str(i[1]) + "," + str(i[0]) for i in ans_path]))
				else:
					if ans_path==None:
						f1.write('FAIL'+"\n")
					else:
						f1.write(' '.join([str(i[1]) + "," + str(i[0]) for i in ans_path])+"\n")
		elif algo=="A*":
			src=(Y,X)
			for i in range(N):
				dest1,dest2=targetx[i],targety[i]
				dest=(dest2,dest1)
				ans_path=astarfun(src,dest,W-1,H-1,dp,zelev)		
				if i==(N-1):
					if ans_path==None:
						f1.write('FAIL')
					else:
						f1.write(' '.join([str(i[1]) + "," + str(i[0]) for i in ans_path]))
				else:
					if ans_path==None:
						f1.write('FAIL'+"\n")
					else:
						f1.write(' '.join([str(i[1]) + "," + str(i[0]) for i in ans_path])+"\n")
						
		f1.close()
									
if __name__=="__main__":
	start_time = time.time()
	main()
	print("--- %s seconds ---" % (time.time() - start_time))
