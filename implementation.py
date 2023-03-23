import unreal
import math
import random
import os
import csv

seqs= []

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

def checkshottype():
    
    with open('D:\python_unreal\ThesisTestsStuff\shotTypes.txt','r') as f:
        print(f.readline())


def createSeq():
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    all_seqs = asset_reg.get_assets_by_path('/Game/2ndSeq')
    if len(all_seqs) == 0:
        shotNum = '0'
    elif len(all_seqs) ==1:
        shotNum = '1'
    elif len(all_seqs)==2:
        shotNum = '2'
    elif len(all_seqs)==3:
        shotNum = '3'
    else: 
        shotNum = '4'
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
    anim_section.set_range(0,150)
    anim_section.params.animation = alexAnims()
    for cam in cams:
        cam_binding = seq.add_possessable(cam)
    unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(seq)


def randomCam(str):
    if str=='medium':
        distance_offset = 300
    elif str=='closeup':
        distance_offset = 100
    elif str=='wide':
        distance_offset = 1000
    # cam = unreal.CineCameraActor()
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
    all_anims = asset_reg.get_assets_by_path('/Game/alex2/standingAnims')
    randomElement = random.choice(all_anims)
    split_path = randomElement.get_full_name().split('.')
    anim_path = "/"+split_path[1].split('/',1)[1]
    anim_path = unreal.EditorAssetLibrary.load_asset(anim_path)
    return anim_path


def camSelection(selection):
    cam=None
    if selection == 1:
        cam=0
    elif selection == 2:
        cam=2
    elif selection == 3:
        cam=1
    elif selection == 4:
        cam=0
    else:
        print('error')
    print(cam)
    savepos = cams[cam].get_actor_location()
    data = [savepos.x,savepos.y,savepos.z]
    with open('D:\python_unreal\ThesisTestsStuff\camChoices.csv','a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def makeFinalFilm():
    at = unreal.AssetToolsHelpers.get_asset_tools()
    campos=[]
    splitcampos=[]
    with open('D:\python_unreal\ThesisTestsStuff\camChoices.csv','r') as f:
        camchoicespos = csv.reader(f,delimiter=',')
        next(camchoicespos)
        for row in f:
            campos.append(row)
    for pos in campos:
        splitcampos.append(pos.split(','))

    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    all_seqs = asset_reg.get_assets_by_path('/Game/2ndSeq')
    masterseq = at.create_asset(
            asset_name= 'finalFilm',
            package_path='/Game/2ndSeq',
            asset_class=unreal.LevelSequence,
            factory=unreal.LevelSequenceFactoryNew(),
        )
    
    masterseq.set_playback_start(0)
    masterseq.set_playback_end(600)
    for i, cam in enumerate(cams):
        cam_binding = masterseq.add_possessable(cam)
        camloc = unreal.Vector(float(splitcampos[i][0]),float(splitcampos[i][1]),float(splitcampos[i][2]))
        cam.set_actor_location(camloc,False,False)
        cameracutsTrack = masterseq.add_master_track(unreal.MovieSceneCameraCutTrack)
        cameracutsSection = cameracutsTrack.add_section()
        if i == 0:
            cameracutsSection.set_range(0,150)
        if i == 1:
            cameracutsSection.set_range(150,300)
        if i == 2:
            cameracutsSection.set_range(300,450)
        if i == 3:
            cameracutsSection.set_range(450,600)

        camBindingID = unreal.MovieSceneObjectBindingID()
        camBindingID.set_editor_property('guid',cam_binding.get_id())
        cameracutsSection.set_camera_binding_id(camBindingID)

        shottrack = masterseq.add_master_track(unreal.MovieSceneCinematicShotTrack)
        shotsection = shottrack.add_section()
        if i == 0:
            shotsection.set_range(0,150)
        if i == 1:
            shotsection.set_range(150,300)
        if i == 2:
            shotsection.set_range(300,450)
        if i == 3:
            shotsection.set_range(450,600)

        split_path = all_seqs[i].get_full_name().split('.')
        seq = "/"+split_path[1].split('/',1)[1]
        seqload = unreal.EditorAssetLibrary.load_asset(seq)
        shot = shotsection.set_sequence(seqload)
    unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(masterseq)

