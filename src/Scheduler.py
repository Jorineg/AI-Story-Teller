from threading import Thread
import traceback
import logging

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, store_result, get_result, on_error=None):
        self.__store_result = store_result
        self.__get_result = get_result
        self.__tasks = []
        self.__abort = False
        self.__on_error = on_error

    def abort(self):
        self.__tasks = []
        self.__abort = True

    def addTask(
        self,
        task,
        arg_list=[],
        result_name=None,
        callback=None,
        incremental=None,
        run_on_main_thread=False,
    ):
        self.__tasks.append(
            (task, result_name, arg_list, callback, incremental, run_on_main_thread)
        )
        self.startTasks()

    def startTasks(self):
        tasks_list = [*self.__tasks]
        for task in tasks_list:
            (
                function,
                result_name,
                arg_list,
                callback,
                incremental,
                run_on_main_thread,
            ) = task
            args = [self.__get_result(arg) for arg in arg_list]
            if any(arg == None for arg in args):
                continue
            try:
                self.__tasks.remove(task)
            except ValueError:
                # task was already removed by another thread (probably)
                # lets start over to make sure we don't miss any tasks
                self.startTasks()
                return

            function_name = function.__name__

            def threadFunc(
                thread_function_name,
                thread_function,
                thread_result_name,
                thread_function_args,
                thread_callback,
                thread_incremental,
            ):
                logger.info(
                    f"Starting task {thread_function_name} to generate {thread_result_name}"
                )
                if thread_incremental:
                    thread_function_args = [
                        thread_incremental,
                        *thread_function_args,
                    ]
                try:
                    thread_result = thread_function(*thread_function_args)
                except Exception as e:
                    logger.critical(
                        f"Error in {thread_function_name} to generate {thread_result_name}:",
                        exc_info=True,
                    )
                    thread_result = None
                    logger.info("aborting...")
                    self.abort()
                    if self.__on_error is not None:
                        self.__on_error(e)

                if thread_result_name is not None and thread_result is not None:
                    self.__store_result(thread_result_name, thread_result)
                if self.__abort:
                    return
                if thread_callback is not None:
                    thread_callback(thread_result)
                self.startTasks()
                logger.info(
                    f"Finished task {thread_function_name} to generate {thread_result_name}"
                )

            thread_args = (
                function_name,
                function,
                result_name,
                args,
                callback,
                incremental,
            )
            if run_on_main_thread:
                threadFunc(*thread_args)
            else:
                thread = Thread(
                    target=threadFunc,
                    args=thread_args,
                )
                thread.start()

            self.startTasks()
            return
