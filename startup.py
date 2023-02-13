import unreal
import sys 
from datetime import datetime 

unreal.log('yoooo')

def test():
    print('calling a method')

def cubeSpawn():
    #cam_class = unreal.CineCameraActor
    cube_mesh = unreal.load_asset("/Game/StarterContent/Shapes/Shape_Cube")
    print(cube_mesh)
    cube_location = unreal.Vector(0.0,0.0,0.0)
    cube_rotation = unreal.Rotator(0.0,0.0,0.0)
    unreal.EditorLevelLibrary.spawn_actor_from_object(cube_mesh,cube_location,cube_rotation)

def assetInfo():
    
    @unreal.uclass()
    class globalEditor(unreal.GlobalEditorUtilityBase):
        pass

    selectedAssets = globalEditor().get_selected_assets()

    for assets in selectedAssets:
        # print(assets.get_name())
        print(assets.get_outer())
        # print(assets.get_path_name())
        #print(assets.get_class())
        print('_______________________________')


def createAsset():
    blueprintName = 'ActorBP'
    bluePrintPath = '/Game/bp'

    #assets are created with factories
    bpFactory = unreal.BlueprintFactory()
    bpFactory.set_editor_property('ParentClass', unreal.Actor)

    assetTools = unreal.AssetToolsHelpers.get_asset_tools()

    myFile = assetTools.create_asset(blueprintName,bluePrintPath,None,bpFactory)

    unreal.EditorAssetLibrary.save_loaded_asset(myFile)

#command line arguements 

def createAssetInput(assetCount,assetName):

    assetName += '%d' #%d number literal

    bluePrintPath = '/Game/bp'
    #assets are created with factories
    bpFactory = unreal.BlueprintFactory()
    bpFactory.set_editor_property('ParentClass', unreal.Actor)


    assetTools = unreal.AssetToolsHelpers.get_asset_tools()

    for x in range(assetCount):

        myFile = assetTools.create_asset(assetName%(x),bluePrintPath,None,bpFactory)
        unreal.EditorAssetLibrary.save_loaded_asset(myFile)

    
def takeSS():
    @unreal.uclass()
    class autoLib(unreal.AutomationLibrary):
        pass

    timeNow = datetime.now().strftime('%H%M%S')
    autoLib.take_high_res_screenshot(1080,720,"_"+timeNow+'.png',None,False,False,unreal.ComparisonTolerance.LOW)
 

def actorCameraSpawn(amt):
    #editor asset library classes do most of the common functionalities with the content browser
    mesh_path = unreal.EditorAssetLibrary.load_asset('/Game/Characters/Mannequin_UE4/Meshes/SK_Mannequin')
    mesh_location = unreal.Vector(0.0,0.0,0.0)
    mesh_rotation = unreal.Rotator(0.0,0.0,0.0)

    for mesh in range(amt):
        unreal.EditorLevelLibrary.spawn_actor_from_object(mesh_path,mesh_location,mesh_rotation)
        mesh_location+=(250,0,0)

    LevelActors = unreal.EditorLevelLibrary.get_all_level_actors()
    #print(unreal.SkeletalMeshActor.static_class())
    for actor in LevelActors:
        if(actor.get_class()==unreal.SkeletalMeshActor.static_class()):
            cam = unreal.CineCameraActor
            cam_location = actor.get_actor_location() + (actor.get_actor_right_vector() * 200)
            cam_location.z +=150
            #cam_rotation = actor.get_actor_rotation()
            cam_rotation = (0,-90,0)
            #takeSS(actor.get_name()) 

            unreal.EditorLevelLibrary.spawn_actor_from_class(cam,cam_location,cam_rotation)
                  

def tagAnim():
    