## **How to activate a virtual python environment on Windows?**

1) Navigate to desired env - open a terminal and make the current working directory to be directory of the env you want to activate. 
2) Check for activated environments - if you see `(.venv) path>` in the terminal it means that a python env is already activated. If `path` is not the path to the desired env make sure you deactivate the env by executing `deactivate`. If `path` matches the path to the desired env you don't have to execute the following steps as it is already activated.
3) Activate the env - in the terminal write the path to the env. For instance if the env is located in the current working directory and if its name is `.venv` this command `.venv\Scripts\activate.bat` should activate the env. If the env is activated successfully the name of its folder should appear in brackets right before the current working directory (for instance `(.venv) E:\Username\Projects\Project1>`). 
4) Verification - to verify whether python uses the env, type `where python` and after that `pip --version`. If those commands return the path to the env you wanted to activate then the env is activated successfully. Note that `where python` may return more than 1 path and if so python will use the first path from the list. 


**Note:** If the above steps don't help refer to Python's documentation or similar source.