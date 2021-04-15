# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 23:47:56 2021

@author: Mike
"""
import numpy as np
import random
from statistics import mean
import scipy.stats
import matplotlib.pyplot as plt
from matplotlib import colors


class Percolation:
    def __init__(self, n):
        self.siteState = np.zeros((n,n))
        
        self.n = n
        
        self.id = np.zeros((n**2)+2)
        for i in range(0,(n**2)+2):
            if i > 0 and i < n+1:
                self.id[i] = 0
                
            elif i < (n**2)+1 and i > n*(n-1):
                self.id[i] = (n**2)+1
               
            else:
                self.id[i] = i
                
        
    

                
    def root(self,i):
        while i != int(self.id[i]):
            self.id[i] = int(self.id[int(self.id[i])])
            i = int(self.id[i])
            
        return int(self.id[i])
            
        
    def connected(self,p,q):
        return self.root(p) == self.root(q)
    
    def union(self,p,q):
        if p<=0 or p>=(self.n**2)+1 or q<=0 or q>=(self.n**2)+1:
            print('Enter a valid p and q')
        elif self.root(p)==0:
            self.id[self.root(q)] = self.id[self.root(p)]
        elif self.root(q)==0:
            self.id[self.root(p)] = self.id[self.root(q)]
        else:
            self.id[self.root(p)] = self.id[self.root(q)]
                
    
        
            
    def openSite(self,i,j):
        if self.siteState[i,j] == 0:
            self.siteState[i,j] = 1
            openedSite = i*self.n+j+1
            #site on top
            if i-1>=0 and self.siteState[i-1,j] == 1:
               qNew =  (i-1)*self.n+j+1
               
               self.union(openedSite,qNew)
            
            #site below
            if i+1<=self.n-1 and self.siteState[i+1,j] == 1:
                qNew = (i+1)*self.n+j+1
                self.union(openedSite,qNew)
            
            #site left
            if j-1>=0 and self.siteState[i,j-1] == 1:
                qNew = (i)*self.n+j-1+1
                self.union(openedSite,qNew)
                
            #site right
            if j+1<=self.n-1 and self.siteState[i,j+1] == 1:
                qNew = (i)*self.n+j+1+1
                self.union(openedSite,qNew)
            
               
    def isOpen(self,i,j):
           if self.siteState[i,j] == 1:
               print('Site ['+ str(i)+','+str(j)+'] is open!')
    
           else:
                print('Site ['+ str(i)+','+str(j)+'] is closed!')
                
    def isFull(self,i,j):
        if self.root(i*self.n+j+1)==0:
            return True    
        else:
            return False                        
        
    def numberOfOpenSites(self):
        return  np.sum(np.count_nonzero(self.siteState == 1,1))

    def percolates(self):
        if self.root(self.n**2+1)==0:
            
            return True
        else:
            
            return False
            

class PercolationStats:
    def __init__(self, N, numSims):
        self.percThreshold =[]
        self.n = N
        
        for i in range(0,numSims):
            self.percObj = Percolation(N)
            fig, ax = plt.subplots()
            cmap = colors.ListedColormap(['red', 'blue', 'green'])
            bounds = [0,.9,.95,1.1,1.9,2.1]
            norm = colors.BoundaryNorm(bounds, cmap.N)
            
            
            ax.imshow(self.percObj.siteState, cmap=cmap, norm=norm)
            
            # draw gridlines
            ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
            
            
            while self.percObj.percolates() == False:
                
                stillClosed = np.where(self.percObj.siteState == 0)
                siteToOpen = random.choice(np.arange(0,stillClosed[0].shape[0]))
                siteToOpenInd = [stillClosed[0][siteToOpen],stillClosed[1][siteToOpen]]
                
                self.percObj.openSite(siteToOpenInd[0],siteToOpenInd[1])
                
                
                
                
                plt.cla()
                ax.imshow(self.percObj.siteState, cmap=cmap, norm=norm)
                                # create discrete colormap
                
                
                plt.show()
                plt.pause(.1)
            self.percThreshold = np.append(self.percThreshold,self.percObj.numberOfOpenSites()/self.percObj.n**2)
            for i in range(0,self.n):
                for j in range(0,self.n):
                    if self.percObj.isFull(i,j) and self.percObj.siteState[i,j]==1:
                        self.percObj.siteState[i,j] = 2
            
            
            
            
            plt.cla()
            ax.imshow(self.percObj.siteState, cmap=cmap, norm=norm)
            plt.show()    
            plt.pause(3) 
            plt.close()
            
        
        self.sampleMean = mean(self.percThreshold)        
        self.std = np.std(self.percThreshold)
        self.CI = self.confidence_interval()
        print('The Mean is: ' + str(self.sampleMean))
        print('The Standard Deviation is: '+ str(self.std))
        print('The 95% confidence interval is: ' + str(self.CI[1]) + ',' + str(self.CI[2]))
    
    
    
    def confidence_interval(self, confidence=0.95):
        data = self.percThreshold
        a = 1.0 * np.array(data)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
        return m, m-h, m+h


            

        
        