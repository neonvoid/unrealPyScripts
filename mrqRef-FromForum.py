import unreal
import os

umap = '/Game/PythonEmptyTest'
level_sequence='/Game/sequences/lvl_sequence0'
level_seq2 = '/Game/sequences/lvl_sequence1'
outdir1=os.path.abspath(os.path.join(unreal.Paths().project_dir(),'out1'))
outdir2=os.path.abspath(os.path.join(unreal.Paths().project_dir(),'out2'))
fps=60
frame_count = 120

#Get movie queue subsystem for editor.
subsystem=unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
q=subsystem.get_queue()


#Optional: empty queue first.
for j in q.get_jobs():
    q.delete_job(j)

#Create new movie pipeline job
job = q.allocate_new_job()
job.set_editor_property('map',unreal.SoftObjectPath(umap))
job.set_editor_property('sequence',unreal.SoftObjectPath(level_sequence))

# job2 = q.allocate_new_job()
# job2.set_editor_property('map',unreal.SoftObjectPath(umap))
# job2.set_editor_property('sequence',unreal.SoftObjectPath(level_seq2))


c=job.get_configuration()
render_pass_settings=c.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
output_setting=c.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
output_setting.output_directory=unreal.DirectoryPath(outdir1)
png_setting=c.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)

# d=job2.get_configuration()
# render_pass_settings=d.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
# output_setting=d.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
# output_setting.output_directory=unreal.DirectoryPath(outdir2)
# png_setting=d.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)


error_callback=unreal.OnMoviePipelineExecutorErrored()
def movie_error(pipeline_executor,pipeline_with_error,is_fatal,error_text):
    print(pipeline_executor)
    print(pipeline_with_error)
    print(is_fatal)
    print(error_text)
error_callback.add_callable(movie_error)
def movie_finished(pipeline_executor,success):
    print(pipeline_executor)
    print(success)
finished_callback=unreal.OnMoviePipelineExecutorFinished()
finished_callback.add_callable(movie_finished)

subsystem.render_queue_with_executor(unreal.MoviePipelinePIEExecutor)
if executor:
    executor.set_editor_property('on_executor_errored_delegate',error_callback)
    executor.set_editor_property('on_executor_finished_delegate',finished_callback)