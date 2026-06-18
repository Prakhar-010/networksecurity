from setuptools import find_packages,setup
from typing import List


def get_requirements()->List[str]:
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                ##ignore the empty lines and -e.
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    
    
    except FileExistsError:
        print("requirements.txt file not find")
        
        
    return requirement_lst
setup(
      name="Network Security",
      version="0.0.1",
      author="Prakhar Awasthi",
      author_email="itsprakhar010@gmail.com",
      packages=find_packages(),
    install_requires=get_requirements()
  )

print(get_requirements())