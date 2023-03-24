import unreal
import random 
import math
from itertools import cycle
import csv

ELL = unreal.EditorLevelLibrary()
EAL = unreal.EditorAssetLibrary()
def spawnCam():
    cam = unreal.CineCameraActor().get_class()
    allActors = ELL.get_all_level_actors()
    print(allActors)
    meshes = []
    cams = []
    for actor in allActors:
        #print(actor.get_class().get_name())
        if actor.get_class().get_name() == "BP_MH_C":
            meshes.append(actor)
    for actor in meshes:
        bounds = actor.get_actor_bounds(False)
        location = actor.get_actor_location() + (actor.get_actor_right_vector()*200)
        location.z = bounds[1].z*2-random.randrange(20,45)
        location.x += random.randrange(-20,20)
        rotation = unreal.Rotator(0,0,-90)
        #rotation = unreal.Rotator(random.randrange(-25,25),0,-90)
        camera = ELL.spawn_actor_from_class(cam,location,rotation,transient=False)
        cams.append(camera)   
    return meshes, cams


def createSequencer(nums,cameraDistance,queueSet):

    KeijiPath = EAL.load_blueprint_class('/Game/MetaHumans/Keiji/BP_Keiji')
    ValPath = EAL.load_blueprint_class('/Game/MetaHumans/Valerie/BP_Val')
    MylesPath = EAL.load_blueprint_class('/Game/MetaHumans/Myles/BP_Myles')
    OskarPath = EAL.load_blueprint_class('/Game/MetaHumans/Oskar/BP_Oskar')
    HudsonPath = EAL.load_blueprint_class('/Game/MetaHumans/Hudson/BP_Hudson')
    LexiPath = EAL.load_blueprint_class('/Game/MetaHumans/Lexi/BP_Lexi')
    VivianPath = EAL.load_blueprint_class('/Game/MetaHumans/Vivian/BP_Vivian')

    mhpaths = [HudsonPath,LexiPath]#[MylesPath,OskarPath]#[KeijiPath,ValPath,MylesPath,OskarPath,HudsonPath,LexiPath,VivianPath]
    mhCycler = cycle(mhpaths)

    alex = EAL.load_asset('/Game/anims/alexwboxes')
    cubeAlex = EAL.load_blueprint_class('/Game/anims/BP_cubeAlex')
    alexspawn = ELL.spawn_actor_from_object(alex,location=unreal.Vector(0,0,0),rotation=unreal.Rotator(0,0,0))
    alexspawn2 = ELL.spawn_actor_from_class(cubeAlex,location=unreal.Vector(0,0,0),rotation=unreal.Rotator(0,0,0))
    attachCube = EAL.load_asset('/Game/anims/attachCube')
    attachCubeSpawn = ELL.spawn_actor_from_object(attachCube,location=unreal.Vector(0,0,0),rotation=unreal.Rotator(0,0,0))
    attachCubeSpawn.set_mobility(unreal.ComponentMobility.MOVABLE)
    # attachCubeSpawn.attach_to_actor(alexspawn2,'Alex_Neck',unreal.AttachmentRule.SNAP_TO_TARGET,unreal.AttachmentRule.SNAP_TO_TARGET,unreal.AttachmentRule.KEEP_RELATIVE,False)
    # #anim_assets= metahumanAnims.anim_assets
    #cycler=cycle(anim_assets) 

    #cam = unreal.CineCameraActor().get_class()
    # camLocation = unreal.Vector(0,300,130)
    # camRotation = unreal.Rotator(0,0,-90)
    # camSpawn = ELL.spawn_actor_from_class(cam,camLocation,camRotation,transient=False)
    
    sequenceName = 'lvl_sequence' + '%d' #+'%d'#'%s'
    sequencerPaths = []
    sequencerWorlds = []
    #for i,(mesh,cam) in enumerate(zip(meshes,cams)):
    for i in range(nums):
        currWorld = alexspawn.get_world().get_name()
        assetTools = unreal.AssetToolsHelpers.get_asset_tools()
        sequence = assetTools.create_asset(asset_name=sequenceName%(i),
                                            package_path='/Game/sequences/',
                                            asset_class=unreal.LevelSequence,
                                            factory=unreal.LevelSequenceFactoryNew())
        randStart = random.randrange(40,150)
        sequence.set_playback_start(randStart)
        sequence.set_playback_end(randStart+30)
        #adding the mesh into the sequencer
        mesh_binding = sequence.add_spawnable_from_instance(next(mhCycler))
        alex_binding = sequence.add_possessable(alexspawn)
        
        alex_bindingTrack = sequence.add_possessable(alexspawn2)
        cubeSpawnTrack = sequence.add_possessable(attachCubeSpawn)

        cubeAttachTrack = cubeSpawnTrack.add_track(unreal.MovieScene3DAttachTrack)
        cubeAttachSection = cubeAttachTrack.add_section()
        cubeAttachSection.set_editor_property('constraint_binding_id',alex_bindingTrack.get_binding_id())
        cubeAttachSection.set_editor_property('attach_component_name',"SkeletalMesh")
        cubeAttachSection.set_editor_property('attach_socket_name',"Alex_Head")
        # camLoc = camSpawn.get_actor_location()
        # camLoc.z += random.randrange(-55,55)
        # camLoc.x += random.randrange(-35,35)
        # camSpawnLoop = ELL.spawn_actor_from_object(camSpawn,camLoc,camRotation)
        camSpawn = randomCircleSpawn(cameraDistance)#+random.randrange(-5,5))
        camera_binding = sequence.add_possessable(camSpawn)
        alex_binding.set_parent(mesh_binding)

        #adding a animtrack
        anim_track = mesh_binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)
        anim_track2 = alex_bindingTrack.add_track(unreal.MovieSceneSkeletalAnimationTrack)
        #adding section to track to manipulate range and params
        anim_section = anim_track.add_section()
        anim_section2 = anim_track2.add_section()
        start_frame = 0#sequence.get_playback_start()-random.randrange(50,70)
        end_frame = sequence.get_playback_end()
        #adding an anim to the track
        anim_section.set_range(start_frame,end_frame)
        anim_section2.set_range(start_frame,end_frame)
        cubeAttachSection.set_range(start_frame,end_frame)
        animforthisloop = assetWalk()
        anim_section.params.animation = animforthisloop
        anim_section2.params.animation = animforthisloop
        #add camera cuts master track
        cameraCutsTrack = sequence.add_master_track(unreal.MovieSceneCameraCutTrack)
        cameraCutsSection = cameraCutsTrack.add_section()
        cameraCutsSection.set_range(start_frame,end_frame)
        #adding camera 
        camera_binding_id = unreal.MovieSceneObjectBindingID()
        camera_binding_id.set_editor_property('guid',camera_binding.get_id())
        cameraCutsSection.set_camera_binding_id(camera_binding_id)

        sequencerPaths.append(sequence.get_path_name())
        sequencerWorlds.append(currWorld)


    return sequencerPaths, sequencerWorlds

    #to try to straighten the above code out a little bit
    #we created a level sequence object called sequence
    #level sequence inherits from movieSceneSequence which has a add_track and add_master_track method 
    #movieSceneSequence also has add_possessable method in it which is how we add possessable objects in our new sequencer
    #which returns a moviescenebindingproxy object
    #in that class there's a add track method which requires a moviescene track class type obj to create a new track
    #which is why we're inputting the class and not creating an instance of it
    #it returns a moviescenetrack object

    #movieSceneSequence also has a add_master_track method with asks for a umoviescenetrack class and returns moviescene track
     
def levelTravel():
    ELL.save_current_level()
    currLev = ELL.get_editor_world().get_name()

    if currLev == 'PythonEmptyTest':
        ELL.load_level('/Game/pink')
    else:
        ELL.load_level('/Game/PythonEmptyTest')

def main(*params):
    seqNum,camDist,qs = params
    #spawnMH(params)
    #meshes,cams = spawnCam()
    seqpaths, seqworlds = createSequencer(seqNum,camDist,qs)
    return seqpaths,seqworlds


def assetWalk():
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    all_anims = asset_reg.get_assets_by_path('/Game/anims/anims')
    randomElement = random.choice(all_anims)
    split_path = randomElement.get_full_name().split('.')
    anim_path = "/"+split_path[1].split('/',1)[1]
    anim_path = unreal.EditorAssetLibrary.load_asset(anim_path)
    return anim_path

def randomCircleSpawn(distance_offset):
    cam = unreal.CineCameraActor()
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
    camRot = unreal.Rotator(0,0,0)
    #camRot = ueMath.find_look_at_rotation(camLoc,centerStage)
    #camRot.pitch = 0
    #print(cam.get_editor_property('lookat_tracking_settings'))
    #print(type(actor))
    #cam.set_editor_property('lookat_tracking_settings',trackingSettings)
    camSpawn = unreal.EditorLevelLibrary().spawn_actor_from_object(cam,camLoc,camRot)
    return camSpawn
    #return camLoc,camRot

def alignTracking():
    allCams = []
    attach = None
    allactors = unreal.EditorLevelLibrary().get_all_level_actors()
    for actor in allactors:
        if actor.get_class().get_name() == 'CineCameraActor':
            allCams.append(actor)
        elif actor.get_name()=='StaticMeshActor_0':
            attach = actor
    
    for cam in allCams:
        trackingSettings = unreal.CameraLookatTrackingSettings()
        trackingSettings.set_editor_property('enable_look_at_tracking',True)
        trackingSettings.set_editor_property("actor_to_track",attach)
        trackingSettings.set_editor_property('look_at_tracking_interp_speed',25)
        cam.lookat_tracking_settings = trackingSettings

    

def randomizeExposure():
    allCams = []
    allactors = unreal.EditorLevelLibrary().get_all_level_actors()
    for actor in allactors:
        if actor.get_class().get_name() == 'CineCameraActor':
            allCams.append(actor)
    
    
    for cam in allCams:
        pps = cam.get_cine_camera_component().get_editor_property('post_process_settings')
        fs = cam.get_cine_camera_component().get_editor_property('focus_settings')
        fb = cam.get_cine_camera_component().get_editor_property('filmback')
        # pps.set_editor_property('override_auto_exposure_method',True)
        # pps.set_editor_property('auto_exposure_method',unreal.AutoExposureMethod.AEM_MANUAL)
        # pps.set_editor_property('override_auto_exposure_bias',True)
        # pps.set_editor_property('auto_exposure_bias',random.uniform(8,12))
        fs.set_editor_property('focus_method',unreal.CameraFocusMethod.DISABLE)
        fb.set_editor_property('sensor_width',12.52)
        fb.set_editor_property('sensor_height',7.58)




def CameraPosDump():
    AllCams= unreal.EditorLevelLibrary.get_all_level_actors()
    file =open('D:\python_unreal\ThesisTestsStuff\datadump.csv','a',newline='')
    writer = csv.writer(file)
    camloc=[]
    for cam in AllCams:
        if cam.get_class().get_name()=='CineCameraActor':
            loc= cam.get_actor_location().to_tuple()
            tempList = [loc[0],loc[1],loc[2]]
            camloc.append(tempList)
    writer.writerows(camloc)
    file.close()



def seqCheck():
    # seq = unreal.EditorAssetLibrary.load_asset('/Game/sequences/lvl_sequence0PythonEmptyTest')
    # seqBindings = seq.get_bindings()
    # for b in seqBindings:
    #     print(b.get_display_name())
    # print(seqBindings[4].get_tracks()[0].get_sections())
    # print(dir(seqBindings[4].get_tracks()[1].get_sections()[0]))
    #print(seqBindings[3].get_tracks()[0].get_sections()[0].get_editor_property('section_range'))
    #MSE = unreal.MovieSceneSectionExtensions()
    #seqBindings[3].get_tracks()[0].get_sections()[0].set_range(0,200)
    asset = unreal.EditorLevelLibrary.get_selected_level_actors()
    print(asset[0])
    trackingSettings = unreal.CameraLookatTrackingSettings()
    trackingSettings.set_editor_property('enable_look_at_tracking',True)
    trackingSettings.set_editor_property("actor_to_track",asset[1])
    trackingSettings.set_editor_property('look_at_tracking_interp_speed',2)
    asset[0].lookat_tracking_settings = trackingSettings
    #al = seqBindings[2]
    # aiBID = al.get_editor_property('binding_id')
    # sections = seqBindings[3].get_tracks()[0].get_sections()
    # compName = sections[0].get_editor_property('attach_component_name')
    # cubeBID = sections[0].get_constraint_binding_id()
    # # print(sections[0].get_editor_property('attach_socket_name'))
    # print(f'name: {al.get_display_name()}, binding id:{al.get_binding_id()}')
    # print(f'name:{type(sections[0])}, binding_id:{cubeBID}')

def test():
    val = EAL.load_blueprint_class('/Game/MetaHumans/Valerie/BP_MH')
    alex = EAL.load_asset('/Game/anims/alexwboxes')
    alexspawn = ELL.spawn_actor_from_object(alex,location=unreal.Vector(0,0,0),rotation=unreal.Rotator(0,0,0))
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    seq = assetTools.create_asset(asset_name='retarget',
                                        package_path='/Game/sequences/',
                                        asset_class=unreal.LevelSequence,
                                        factory=unreal.LevelSequenceFactoryNew())
    print(val)
    print(type(val))

    valbind = seq.add_spawnable_from_instance(val)
    alexbind = seq.add_possessable(alexspawn)
    anim_track = valbind.add_track(unreal.MovieSceneSkeletalAnimationTrack)
    anim_section = anim_track.add_section()
    anim_section.set_range(-50,300)
    anim_section.params.animation = EAL.load_asset('/Game/anims/anims/kick4_01')

    alexbind.set_parent(valbind)

    #rendering the movie out to the saved dir with default capture settings
def render(sequencer):
    for sequencer in sequencer:
        capture_settings = unreal.AutomatedLevelSequenceCapture()
        capture_settings.level_sequence_asset = unreal.SoftObjectPath(sequencer)
        capture_settings.get_editor_property('settings').set_editor_property('output_format','{world}{sequence}')

        unreal.SequencerTools.render_movie(capture_settings,unreal.OnRenderMovieStopped())


def spawnSK(nums):
    SK2filePath = EAL.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple')
    SKfilePath = EAL.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Quinn_Simple')
    for i in range(nums):
        location=unreal.Vector(random.randrange(-1000,1000),random.randrange(-1000,1000),0.0)
        rotation=unreal.Rotator(0.0,0.0,0.0)
        if i%2==0:
            ELL.spawn_actor_from_object(SKfilePath,location,rotation)
        else:
            ELL.spawn_actor_from_object(SK2filePath,location,rotation)

def spawnMH(nums):
    KeijiPath = EAL.load_blueprint_class('/Game/MetaHumans/Keiji/BP_MH')
    ValPath = EAL.load_blueprint_class('/Game/MetaHumans/Valerie/BP_MH')
    MHPaths = [KeijiPath,ValPath]
    cycler=cycle(MHPaths) 
    for i in range(nums):
        location= unreal.Vector(random.randrange(-1000,1000),random.randrange(-1000,1000),0.0)
        rotation= unreal.Rotator(0.0,0.0,0.0)
        #ELL.spawn_actor_from_class(next(cycler),location,rotation)
        
    
def timetest():
    world = unreal.UnrealEditorSubsystem().get_game_world()
    gps = unreal.GameplayStatics()
    gps.set_global_time_dilation(world,5)

def etest():
    level_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    character_actor = None
    for actor in level_actors:
        if actor.get_class().get_name() == "BP_Lexi_C":
            character_actor = actor
            break 
    comps = character_actor.root_component.get_children_components(True)
    cam = None
    for c in comps:
        if c.get_name() == "CineCamera":
            cam = c
    camLoc,camRot = randomCircleSpawn(80)
    print(camLoc)
    cam.set_world_rotation(unreal.Rotator(0,0,-85),False,False)
    cam.set_world_location(camLoc,False,False)

    at = unreal.AssetToolsHelpers.get_asset_tools()
    seq = at.create_asset(
        asset_name= 'test',
        package_path='/Game/Sequences',
        asset_class=unreal.LevelSequence,
        factory=unreal.LevelSequenceFactoryNew(),
    )
    lex_bind = seq.add_possessable(character_actor)
    anim_bind = None
    for comp in comps:
        if comp.get_name() == 'alexwboxes':
            anim_bind = seq.add_possessable(comp)
            anim_bind.set_parent(lex_bind)
        elif comp.get_name() == 'CineCamera':
            cam_bind = seq.add_possessable(comp)
            cam_bind.set_parent(lex_bind)
        else:
            track = seq.add_possessable(comp)
            track.set_parent(lex_bind)
    anim_track = lex_bind.add_track(unreal.MovieSceneSkeletalAnimationTrack)
    anim_section = anim_track.add_section()
    anim_section.params.animation = unreal.EditorAssetLibrary.load_asset('/Game/anims/anims/kick4_01')
    anim_section.set_range(0,seq.get_playback_end())
