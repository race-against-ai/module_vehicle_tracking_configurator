# RAAI Module Template
A GitHub Template for creating modular RAAI Components

## Stuff you need to change
- Change the ```README.md``` according to your project
- rename the ```your_project_folder``` to the name of your project
- edit the ```setup.cfg``` and change `your_project_folder` to the name of your project
- edit ```.gitattributes``` to the new folder
- put your GitHub or Volkswagen email in the ```setup.py```
- import and execute your main file from the project folder into the root ```main.py```
- adjust the ```pyinstaller.spec``` according to your project (mainly the name)

## Config File
Adjust the Config file to your needs. The mandatory name convention for it is "[your_project_name]_config.json" <br>
you can adjust the content in it to your needs

#### Pynng:
If you have Pynng Objects in your code then you need to mark them up in the Config File, an example will already be
inside the Template

If Topics aren't *needed* in your code then they don't have to be written inside. It probably is very self-explanatory<br>
There's no limit for the amount of Objects inside the Config but the "publishers" and "subscribers" tab should always be
inside

Here is the Rough Structure that has to be complied with:

```
config_file
└─── "pynng"
    ├─── "publishers"
    |     └─── "pub_object_1"
    |          ├─── "address": ipc adress
    |          └─── "topics"
    |               └─── "sudo name": "topic_name"
    |
    |
    └─── "subscribers"
          ├─── "sub_object_1"
          |    ├─── "address": ipc adress
          |    └─── "topics"
          |         ├─── "whatever you can remember": "foobar"
          |         └─── "or is easy to use in code": "wha_ever"
          └─── "sub_object_2"
               ├─── "address": ipc adress
               └─── "topics"
                    └─── "sudo name": "topic_name"
    
            
```

## Code Syntax
To test your code type syntax run

```
tox -e type
```

or to check the style syntax run
```
tox -e style
```

to run a lint check, enter
```
tox -e lint_check
```

To update your code when encountering errors on lint check, just run
```
tox -e lint_update
```
