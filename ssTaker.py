import unreal
import os
auto = unreal.AutomationLibrary()

dir = 'D:\python_unreal\ThesisTestsStuff\osc\oscTests/'
def takess():
    for f in os.listdir(dir):
        os.remove(os.path.join(dir,f))
    auto.take_high_res_screenshot(100,100,'ss',None,False,False,unreal.ComparisonTolerance.LOW,'',0.0)
