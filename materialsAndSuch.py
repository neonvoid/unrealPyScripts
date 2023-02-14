import unreal
import random
#get all static mesh actors
#get all materials
#get all textures


def getStaticMesh():
    static_meshes = []
    allActors = unreal.EditorActorSubsystem().get_all_level_actors()
    for asset in allActors:
        if(asset.get_class().get_name() == "StaticMeshActor"):
            print(f'{asset.get_name()} is being added to array')
            static_meshes.append(asset)


    return static_meshes

def get_materials():
    static_meshes = getStaticMesh()
    materials = []
    for meshes in static_meshes:
        mats = meshes.static_mesh_component.get_materials()
        print(mats)

def spawnSK(nums):
    EAL = unreal.EditorAssetLibrary()
    ELL = unreal.EditorLevelLibrary()
    AT = unreal.AssetToolsHelpers.get_asset_tools()

    ueSK = EAL.load_asset('/Game/Characters/Mannequin_UE4/Meshes/SK_Mannequin')
    skeletalMeshes = []
    cineCams = []
    sequence_name = 'lvlSequence' + '%d'

    #spawning skeletal meshes
    for i in range (nums):
        location = unreal.Vector(random.uniform(-1000,1000),random.uniform(-1000,1000),0)
        rotator = unreal.Rotator(0,0,0)
        mesh = ELL.spawn_actor_from_object(ueSK,location,rotator,False)
        skeletalMeshes.append(mesh)

    #spawning a cinecamera for each skeletal mesh
    for mesh in skeletalMeshes:
        cam = unreal.CineCameraActor
        cam_location = mesh.skeletal_mesh_component.relative_location
        cam_location.y += 200
        cam_location.z += random.uniform(140,190)
        cam_rotation = unreal.Rotator(0,0,-90)
        spawnedCam = ELL.spawn_actor_from_class(cam,cam_location,cam_rotation,False)
        cineCams.append(spawnedCam)

    #creating a level sequence for each cine camera/mesh pair
    AT = unreal.AssetToolsHelpers.get_asset_tools()
    i = 0
    for mesh,cam in zip(skeletalMeshes,cineCams):
        
        lvl_seq = unreal.AssetTools.create_asset(AT,sequence_name%(i),package_path='/Game/sequences',
        asset_class= unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())

        #creating a camera cuts track in each sequencer
        #setting the start and stop (5 seconds)
        #adds a master track of camera cuts track
        camera_cut_track = lvl_seq.add_master_track(unreal.MovieSceneCameraCutTrack)
        #moviescenecameracuttrack inherits from moviescenetrack which has a addtrack option
        camera_cut_section = camera_cut_track.add_section()
        camera_cut_section.set_start_frame_seconds(0)
        camera_cut_section.set_end_frame_seconds(5)
        
        #adding a mesh in the sequencer
        lvl_seq.add_possessable(mesh)
        #adding a cine camera in as well
        binding = lvl_seq.add_possessable(cam)

        #creating this binding ID object, setting this variable to the cine cameras ID
        camera_binding_id = unreal.MovieSceneObjectBindingID()
        #setting the instance of this object to the cameras ID
        camera_binding_id.set_editor_property('Guid',binding.get_id())
        camera_cut_section.set_editor_property('CameraBindingID',camera_binding_id)
        i+=1


def createSeq():
    basePath = '/Game/Generics/'
    anim_path = unreal.load_asset("/Game/Characters/Mannequins/Animations/Manny/MM_Run_Fwd")
    manny = unreal.EditorAssetLibrary.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny')
    location = unreal.Vector(0,0,0)
    rotation = unreal.Rotator(0,0,0)
    mesh = unreal.EditorLevelLibrary.spawn_actor_from_object(manny,location,rotation,False)

    
    sequencer = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name='simpleSequencer',
    package_path=basePath,asset_class=unreal.LevelSequence,factory=unreal.LevelSequenceFactoryNew())
    location = unreal.Vector(0,0,0)
    rotation = unreal.Rotator(0,0,0)
    unreal.EditorLevelLibrary.spawn_actor_from_object(sequencer,location,rotation,False)

    actor_binding = sequencer.add_possessable(mesh)
    anim_track = actor_binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)
    anim_section = anim_track.add_section()
    anim_section.params.animation=anim_path
    anim_section.set_range(0, 1000)

    camera_cut_track = sequencer.add_master_track(unreal.MovieSceneCameraCutTrack)
    camera_cut_section = camera_cut_track.add_section()
    camera_cut_section.set_start_frame(0)
    camera_cut_section.set_end_frame(10)
    

def test():
    anim_path = unreal.load_asset("/Game/Characters/Mannequins/Animations/Manny/MM_Run_Fwd")
    print(anim_path.get_editor_property('sequence_length'))


