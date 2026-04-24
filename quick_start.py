from oscopilot import AxelAgent
from oscopilot import ToolManager
from oscopilot import AxelExecutor, AxelPlanner, AxelRetriever
from oscopilot.utils import setup_config, setup_pre_run

args = setup_config()
if not args.query:
    args.query = "Copy any text file located in the working_dir/document directory that contains the word 'agent' to a new folder named 'agents' "
task = setup_pre_run(args)
agent = AxelAgent(AxelPlanner, AxelRetriever, AxelExecutor, ToolManager, config=args)
agent.run(task=task)
