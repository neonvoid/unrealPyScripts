import unreal
import os

auto = unreal.AutomationLibrary()

i=0

def takess():
    global i
    auto.take_high_res_screenshot(100,100,'ss%d'%(i),None,False,False,unreal.ComparisonTolerance.LOW,'',0.0)
    i+=1
