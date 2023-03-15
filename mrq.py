import unreal
import os 
import sequencer
import random

pathVar = []
worldVar = []


def create(num):
    global pathVar
    global worldVar
    pathOut, worldOut = sequencer.main(num)
    pathVar.append(pathOut)
    worldVar.append(worldOut)

#apparently we keep this alive so python doesn't delete it
executor = None
spawnedLight = None
fog = None
outputDir = os.path.abspath(os.path.join(unreal.Paths().project_dir(),'0'))

def OnIndividualJobFinishedCallback(params,success):
    global fog
    fog[0].component.set_fog_inscattering_color((random.uniform(0,10),random.uniform(0,10),random.uniform(0,10)))
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    all_anims = asset_reg.get_assets_by_path('/Game/hdrs')
    randomElement = random.choice(all_anims)
    split_path = randomElement.get_full_name().split('.')
    hdr_path = "/"+split_path[1].split('/',1)[1]
    hdr_path = unreal.EditorAssetLibrary.load_asset(hdr_path)
    ELL = unreal.EditorLevelLibrary()
    actor = ELL.get_all_level_actors()
    for actor in actor:
        if actor.get_class().get_name()== 'HDRIBackdrop_C':
            hdr = actor
    print(hdr.get_editor_property('Cubemap'))
    hdr.set_editor_property('Cubemap',hdr_path)


def mvqDocument(paths,worlds):
    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    ELL = unreal.EditorLevelLibrary()
    queue = subsystem.get_queue()
    # print(queue)
    # print(queue.get_jobs())

    if (len(queue.get_jobs()) > 0):
        for job in queue.get_jobs():
            queue.delete_job(job)

    for i,(path,world) in enumerate(zip(paths,worlds)):
        #print(f'path:{path}, world:{worlds}')
        job = queue.allocate_new_job()
        job.set_editor_property('map',unreal.SoftObjectPath("/Game/"+world))
        job.set_editor_property('sequence',unreal.SoftObjectPath(path))

        jobConfig = job.get_configuration()
        render_pass = jobConfig.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
        output_setting = jobConfig.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
        output_setting.output_directory = unreal.DirectoryPath(outputDir)
        output_setting.output_resolution = (100,100)
        png_output = jobConfig.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)

    global spawnedLight
    global fog
    #spawnedLight = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLight,(0,0,100))
    # spawnedLight.set_brightness(5000)
    # spawnedLight.set_light_color((0,0,1,1))

    allactors = ELL.get_all_level_actors()
    fog = []
    for actor in allactors:
        if actor.get_class().get_name() == 'ExponentialHeightFog':
            fog.append(actor)

    global executor
    executor = unreal.MoviePipelinePIEExecutor()
    callback = unreal.OnMoviePipelineIndividualJobFinished()
    callback.add_callable(OnIndividualJobFinishedCallback)
    executor.set_editor_property('on_individual_job_finished_delegate',callback)
    subsystem.render_queue_with_executor_instance(executor)

    
    # what are soft object paths
    # look through MoviePipelineQueueSubsystem
    # get_editor_subsystem and get_queue
    # OnMoviePipelineExecutorFinished

def render():
    print(worldVar)
    renderWorldVar = worldVar[0] #+worldVar[1]
    renderPathVar = pathVar[0] #+pathVar[1]
    mvqDocument(renderPathVar,renderWorldVar)

def fogColorChangeTest():
    ELL = unreal.EditorLevelLibrary()
    allactors = ELL.get_all_level_actors()
    fog = []
    for actor in allactors:
        if actor.get_class().get_name() == 'ExponentialHeightFog':
            fog.append(actor)
    fog[0].component.set_fog_inscattering_color((random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)))