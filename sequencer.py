import unreal
import random 
from itertools import cycle
#using this file to review and practice first
#spawn just 1 sk and 1 cam, no need for fancy shit
#create a sequencer
#add both the sk and cam into the sequencer
#create a camera cuts master track
#create an anim track
#try to render it out I guess

ELL = unreal.EditorLevelLibrary()
EAL = unreal.EditorAssetLibrary()
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

def spawnCam():
    cam = unreal.CineCameraActor().get_class()
    allActors = ELL.get_all_level_actors()
    meshes = []
    cams = []
    for actor in allActors:
        if actor.get_class().get_name() == "SkeletalMeshActor":
            meshes.append(actor)
    for actor in meshes:
        bounds = actor.get_actor_bounds(False)
        location = actor.get_actor_location() + (actor.get_actor_right_vector()*200)
        location.z = bounds[1].z*2-random.randrange(10,45)
        rotation = unreal.Rotator(random.randrange(-25,25),0,-90)
        camera = ELL.spawn_actor_from_class(cam,location,rotation,transient=False)
        cams.append(camera)   
    return meshes, cams


def createSequencer(meshes, cams):

    anim_assets= [EAL.load_asset("/Game/Characters/Mannequins/Animations/Manny/MM_Jump"),
                  EAL.load_asset('/Game/Characters/Mannequins/Animations/Manny/MM_Run_Fwd'),
                  EAL.load_asset('/Game/Characters/Mannequins/Animations/Manny/MM_Idle')]
    
    cycler=cycle(anim_assets) 
    
    sequenceName = 'lvl_sequence' + '%d' +'%s'
    sequencerPaths = []
    sequencerWorlds = []
    for i,(mesh,cam) in enumerate(zip(meshes,cams)):
        currWorld = mesh.get_world().get_name()
        assetTools = unreal.AssetToolsHelpers.get_asset_tools()
        sequence = assetTools.create_asset(asset_name=sequenceName%(i,currWorld),
                                            package_path='/Game/sequences/',
                                            asset_class=unreal.LevelSequence,
                                            factory=unreal.LevelSequenceFactoryNew())
        #adding the mesh into the sequencer
        mesh_binding = sequence.add_possessable(mesh)
        camera_binding = sequence.add_possessable(cam)
        #adding a animtrack
        anim_track = mesh_binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)
        #adding section to track to manipulate range and params
        anim_section = anim_track.add_section()
        start_frame = sequence.get_playback_start()
        sequence_end = sequence.set_playback_end(50)
        end_frame = sequence.get_playback_end()
        #adding an anim to the track
        anim_section.set_range(start_frame,end_frame)

        anim_section.params.animation = next(cycler)
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

#rendering the movie out to the saved dir with default capture settings
def render(sequencer):
    for sequencer in sequencer:
        capture_settings = unreal.AutomatedLevelSequenceCapture()
        capture_settings.level_sequence_asset = unreal.SoftObjectPath(sequencer)
        capture_settings.get_editor_property('settings').set_editor_property('output_format','{world}{sequence}')

        unreal.SequencerTools.render_movie(capture_settings,unreal.OnRenderMovieStopped())
        
def levelTravel():
    ELL.save_current_level()
    ELL.load_level('/Game/pink')

def main(params):
    spawnSK(params)
    meshes,cams = spawnCam()
    return createSequencer(meshes,cams)

