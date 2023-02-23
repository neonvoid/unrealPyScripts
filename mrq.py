import unreal
import os 

outdir1=os.path.abspath(os.path.join(unreal.Paths().project_dir(),'out1'))
outdir2=os.path.abspath(os.path.join(unreal.Paths().project_dir(),'out2'))

def individJobFinishedCallback(params,sucess):
    print(params)
    print(sucess)

def mvqDocument():
    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    queue = subsystem.get_queue()
    # print(queue)
    # print(queue.get_jobs())

    if (len(queue.get_jobs()) > 0):
        for job in queue.get_jobs():
            queue.delete_job(job)

    map = '/Game/PythonEmptyTest'
    level_sequence='/Game/sequences/lvl_sequence0'

    map2 = '/Game/pink'
    level2_sequence= '/Game/sequences/pinkTest'

    job1 = queue.allocate_new_job()
    job1.set_editor_property('map',unreal.SoftObjectPath(map))
    job1.set_editor_property('sequence',unreal.SoftObjectPath(level_sequence))

    job1config = job1.get_configuration()
    render_pass = job1config.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
    output_setting = job1config.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
    output_setting.output_directory = unreal.DirectoryPath(outdir1)
    png_output = job1config.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)

    job2 = queue.duplicate_job(queue.get_jobs()[0])
    job2.set_editor_property('map',unreal.SoftObjectPath(map2))
    job2.set_editor_property('sequence',unreal.SoftObjectPath(level2_sequence))
    job2config = job2.get_configuration()
    output_setting = job2config.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
    output_setting.output_directory = unreal.DirectoryPath(outdir2)

    #executor = unreal.MoviePipelinePIEExecutor()
    #finished_callback = unreal.OnMoviePipelineExecutorFinished()
    #finished_callback.add_callable(individJobFinishedCallback)
    #executor.on_executor_finished_delegate.add_callable_unique(queueFinishedCallback)
    #executor.set_editor_property('on_executor_finished_delegate', finished_callback)

    subsystem.render_queue_with_executor(unreal.MoviePipelinePIEExecutor)


    #what are soft object paths
    #look through MoviePipelineQueueSubsystem
    #get_editor_subsystem and get_queue
    #OnMoviePipelineExecutorFinished