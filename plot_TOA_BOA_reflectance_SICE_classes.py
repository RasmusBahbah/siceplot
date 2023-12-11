# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 11:14:15 2023

@author: rabni
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

if os.getlogin() == 'jason':
    base_path = '/Users/jason/Dropbox/S3/siceplot/'
os.chdir(base_path)

def predefined_colors(classes):
    N_classes=len(classes)
    color_list=np.zeros((N_classes,4))
    color_list[0] = (100/255,100/255,100/255, 1.0)  # dark bare ice
    co=150
    color_list[1] = (co/255,co/255,co/255, 1.0)  # bright bare ice
    color_list[2] = (130/255,70/255,179/255, 1.0)  # purple ice
    color_list[3] = (1,0,0, 1)  # red snow
    color_list[4] = (0.8,0.8,0.3, 1.0)  # lakes
    color_list[5] = (.5,.5,1, 1.0)  # flooded_snow
    color_list[6] = (239/255,188/255,255/255, 1)  # melted_snow
    color_list[7] = (0,0,0, 1.0)  # dry_snow'
    return color_list

# Customize the plot
# graphics definitions
th=2 # line thickness
formatx='{x:,.3f}' ; fs=18
plt.rcParams["font.size"] = fs
plt.rcParams['axes.facecolor'] = 'w'
plt.rcParams['axes.edgecolor'] = 'k'
plt.xticks(fontsize=30, rotation=90)
plt.yticks(fontsize=30)
plt.rcParams['axes.grid'] = False
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.5
plt.rcParams['grid.color'] = "#C6C6C6"
plt.rcParams["legend.facecolor"] ='w'
plt.rcParams["mathtext.default"]='regular'
plt.rcParams['grid.linewidth'] = th/2
plt.rcParams['axes.linewidth'] = 1


toa_mean = pd.read_csv('toa_data.csv')
brr_mean = pd.read_csv('boa_data.csv')
band_wl = pd.read_csv('S3_spectrum.csv')

training_bands = ["rBRR_01" ,"rBRR_02" ,"rBRR_03", "rBRR_04", "rBRR_05","rBRR_06" ,"rBRR_07" ,"rBRR_08", "rBRR_09",\
          "rBRR_10" ,"rBRR_11" ,"rBRR_16" ,"rBRR_17", "rBRR_18", "rBRR_19"\
          ,"rBRR_21" ]
    
classes = ['dark_ice','bright_ice','purple_ice','red_snow','lakes','flooded_snow','melted_snow','dry_snow']
n_classes=len(classes)

n_bands=(16)

color_multi = predefined_colors(classes)

start = 1

comb = [1,2,3]
# comb = [1]
# Plot the line
# the text bounding box
bbox = {'fc': '0.8', 'pad': 0}

nams=['TOA','rBRR']

for cc in comb:   
    refl=np.zeros((n_classes,n_bands))

    # Initialize a figure
    fig, ax = plt.subplots(figsize=(12, 12))
    start = 1
    for i,c in enumerate(classes):
        
        bands = [tb[-2:] for tb in training_bands] 
        x = np.array([band_wl[b] for b in bands])
        y = toa_mean[c][0]
        y = np.array(y.strip('][').split(', ')).astype(float)
     
        y1 = brr_mean[c][0]
        y1 = np.array(y1.strip('][').split(', ')).astype(float)
        #z = np.array(toa_mean[c]['std'])
    
        if cc == 1:
            dat_plot = y
            ann = -0.0
            ann_y = 1
            ylabel = 'TOA reflectance'
            f_n = 'toa_of_training_data'
        elif cc == 2:
            ann = -0.0
            ann_y = 1
            dat_plot = y1
            ylabel = 'BOA reflectance'
            f_n = 'boa_of_training_data'
        elif cc == 3:
            dat_plot = y1/y
            ann = 0.6
            ann_y = 1.82
            ylabel = 'BOA/TOA Ratio'
            f_n = 'boa_toa_ratio_of_training_data'
        
        refl[i,:]=dat_plot
        ax.scatter(x, dat_plot,label=f'{c}',color = color_multi[i],s=40)
        ax.scatter(x, dat_plot,color = 'black',s=45,zorder=0)
        # Create shaded area around the line
        #ax.fill_between(x, y - z, y + z, alpha=0.3, color=color_multi[i])
        ax.plot(x, dat_plot,color = color_multi[i],zorder=0,linewidth = 1)
        ax.plot(x, dat_plot,color = 'black',zorder=-1,linewidth = 2)
    
        if start == 1 and c == 'red_snow':
            for ii, txt in enumerate(training_bands):
                ax.annotate('B'+txt[-2:], (x[ii], ann),
                 rotation=90,zorder=5,size = 15)
                ax.plot((x[ii],x[ii]), (ann,ann_y),color = 'black',alpha=0.2,
                        zorder=-5)
            start = 0
                
    ax.set_xlabel('wavelength, nm',fontsize=fs)
    ax.set_ylabel(ylabel,fontsize=fs)
    #ax.set_title('Mean Reflectance on Training Data',fontsize=35)
    ax.legend(loc='center left',bbox_to_anchor=(1,0.5),fontsize=fs,markerscale=4)
    # Show the plot

    ly='p'

    if ly == 'x':plt.show()
    
    if ly == 'p':
        DPI=300
        path_Figs='./Figs/'
        os.system('mkdir -p '+path_Figs)
        figname=f'./Figs/{f_n}.png'
        plt.savefig(figname, bbox_inches='tight', dpi=DPI, facecolor='w')
        # os.system('open '+figname)
        
        
    if cc<2:
        out=pd.DataFrame({'lamda':x.flatten(),
                      classes[0]:refl[0,:],
                      classes[1]:refl[1,:],
                      classes[2]:refl[2,:],
                      classes[3]:refl[3,:],
                      classes[4]:refl[4,:],
                      classes[5]:refl[5,:],
                      classes[6]:refl[6,:],
                      classes[7]:refl[7,:],
                      })
    
        out.to_csv(nams[cc]+'_classes_refl.csv',index=None)