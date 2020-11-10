#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np

# for use with https://github.com/LingDong-/linedraw


# In[9]:


tree = ET.parse("out.svg")


# In[74]:


lines=[]
for child in tree.getroot():
    l=[float(x) for x in child.attrib["points"].split(",")]
    p=[[l[(2*n)],l[(2*n)+1]] for n in range(0,int(len(l)/2))]
    print(p)
    lines.append(p)


# In[81]:


lnp=np.array(lines)

for n in range(0,len(lnp)):
    plt.plot(np.array(lnp[n]).T[0],-np.array(lnp[n]).T[1])

