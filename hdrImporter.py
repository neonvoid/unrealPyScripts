import unreal
import skyboxAPI
import os

def runSkybox(prompt,num):
    filepath = skyboxAPI.main(prompt,num)
    return filepath

def prepImport(filepath, callback):
    hdr1UE = buildingTasks(filepath)
    executeImports([hdr1UE])
    ID = (os.path.split(filepath)[1]).split('.')[0]
    callback(ID)

def buildingTasks(filename):
    AI = unreal.AssetImportTask()
    AI.set_editor_property('automated',True)
    AI.set_editor_property('destination_path', '/Game/hdrs')
    AI.set_editor_property('replace_existing',False)
    AI.set_editor_property('save',True)
    AI.set_editor_property('filename',filename)
    return AI

def executeImports(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

def setHDRI(ID):
    #"D:\thesisMeshesandAnims\hdris\772441.hdr"
    asset_path = f'/Game/hdrs/{ID}'
    hdriFilePath=unreal.EditorAssetLibrary.load_asset(asset_path)
    ELL = unreal.EditorLevelLibrary()
    actor = ELL.get_all_level_actors()
    for actor in actor:
        if actor.get_class().get_name()== 'HDRIBackdrop_C':
            hdr = actor
    
    #print(dir(hdr))
    # hdrRot = hdr.get_actor_rotation()
    # hdrRot.yaw += 30
    # hdr.set_actor_rotation(hdrRot, False)

    print(hdr.get_editor_property('Cubemap'))
    hdr.set_editor_property('Cubemap',hdriFilePath)

def main(prompt,num):
    total_frames = 1
    text_label = 'calling skybox api and generating'
    with unreal.ScopedSlowTask(total_frames,text_label, enabled=True) as slow:
        slow.make_dialog(True)
        for i in range(total_frames):
            slow.enter_progress_frame(work=1,desc="downloading")

            filepath = runSkybox(prompt,num)
            prepImport(filepath,setHDRI)