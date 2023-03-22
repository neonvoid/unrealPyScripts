import unreal
import math
import random
import os

def checkshottype():
    with open('D:\python_unreal\ThesisTestsStuff\shotTypes.txt','r') as f:
        print(f.readline())

#get alex
allactors = unreal.EditorLevelLibrary().get_all_level_actors()
alex = None
attach = None
cams = []
for actor in allactors:
    if actor.get_class().get_name()=='SkeletalMeshActor':
        alex = actor
    elif actor.get_class().get_name()=="CineCameraActor":
        cams.append(actor)
    elif actor.get_name()=='StaticMeshActor_0':
        attach = actor

def createSeq(shotNum):
    at = unreal.AssetToolsHelpers.get_asset_tools()
    seq_names = shotNum
    seq = at.create_asset(
            asset_name= seq_names,
            package_path='/Game/2ndSeq',
            asset_class=unreal.LevelSequence,
            factory=unreal.LevelSequenceFactoryNew(),
        )
    alex_bind = seq.add_possessable(alex)
    anim_track = alex_bind.add_track(unreal.MovieSceneSkeletalAnimationTrack) 
    anim_section = anim_track.add_section()
    anim_section.set_range(0,50)
    anim_section.params.animation = alexAnims()
    for cam in cams:
        cam_binding = seq.add_possessable(cam)

def randomCam(distance_offset):
    #cam = unreal.CineCameraActor()
    for cam in cams:
        vertCount = 1000
        step=2*math.pi/vertCount
        theta = random.randrange(0,vertCount)
        theta *= step
        x = math.cos(theta) * distance_offset
        y = math.sin(theta) * distance_offset

        #centerStage = unreal.Vector(0,0,0)
        camLoc=unreal.Vector(x,y,random.randrange(100,170))
        camLoc.y += random.randrange(-50,50)
        camLoc.x += random.randrange(-35,35)
        camLoc.z +=random.randrange(10,100)
        #camRot = ueMath.find_look_at_rotation(camLoc,centerStage)
        #camRot.pitch = 0
        #print(cam.get_editor_property('lookat_tracking_settings'))
        #print(type(actor))
        #cam.set_editor_property('lookat_tracking_settings',trackingSettings)
        #return camLoc,camRot
        cam.set_actor_location(camLoc,False,False)
    alignTracking()


def alignTracking():
    for cam in cams:
        trackingSettings = unreal.CameraLookatTrackingSettings()
        trackingSettings.set_editor_property('enable_look_at_tracking',True)
        trackingSettings.set_editor_property("actor_to_track",attach)
        trackingSettings.set_editor_property('look_at_tracking_interp_speed',10)
        cam.lookat_tracking_settings = trackingSettings

def alexAnims():   
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    all_anims = asset_reg.get_assets_by_path('/Game/alex/anims')
    randomElement = random.choice(all_anims)
    split_path = randomElement.get_full_name().split('.')
    anim_path = "/"+split_path[1].split('/',1)[1]
    anim_path = unreal.EditorAssetLibrary.load_asset(anim_path)
    return anim_path