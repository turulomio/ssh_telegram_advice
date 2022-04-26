from setuptools import setup, Command
import site
import os
import platform

class Reusing(Command):
    description = "Fetch remote modules"
    user_options = [
      # The format is (long option, short option, description).
      ( 'local', None, 'Update files without internet'),
  ]

    def initialize_options(self):
        self.local=False

    def finalize_options(self):
        pass

    def run(self):
        from sys import path
        path.append("ssh_telegram_advice/reusing")
        if self.local is False:
            from github import download_from_github
            download_from_github('turulomio','reusingcode','python/github.py', 'ssh_telegram_advice/reusing/')
            download_from_github('turulomio','reusingcode','python/datetime_functions.py', 'ssh_telegram_advice/reusing/')
            download_from_github('turulomio','reusingcode','python/file_functions.py', 'ssh_telegram_advice/reusing/')

## Class to define doc command
class Translate(Command):
    description = "Update translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        #es
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/ssh_telegram_advice.pot *.py ssh_telegram_advice/*.py ssh_telegram_advice/reusing/*.py setup.py")
        os.system("msgmerge -N --no-wrap -U locale/es.po locale/ssh_telegram_advice.pot")
        os.system("msgfmt -cv -o ssh_telegram_advice/locale/es/LC_MESSAGES/ssh_telegram_advice.mo locale/es.po")
        os.system("msgfmt -cv -o ssh_telegram_advice/locale/en/LC_MESSAGES/ssh_telegram_advice.mo locale/en.po")

    
class Procedure(Command):
    description = "Show release procedure"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("""Nueva versión:
  * Cambiar la versión y la fecha en __init__.py
  * Modificar el Changelog en README
  * python setup.py translate
  * linguist
  * python setup.py translate
  * python setup.py uninstall; python setup.py install
  * python setup.py doxygen
  * git commit -a -m 'ssh_telegram_advice-{0}'
  * git push
  * Hacer un nuevo tag en GitHub
  * python setup.py sdist
  * twine upload dist/ssh_telegram_advice-{0}.tar.gz 
  * python setup.py uninstall
  * Crea un nuevo ebuild de ssh_telegram_advice Gentoo con la nueva versión
  * Subelo al repositorio del portage

""".format(__version__))

## Class to define doxygen command
class Doxygen(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Creating Doxygen Documentation")
        os.system("""sed -i -e "41d" doc/Doxyfile""")#Delete line 41
        os.system("""sed -i -e "41iPROJECT_NUMBER         = {}" doc/Doxyfile""".format(__version__))#Insert line 41
        os.system("rm -Rf build")
        os.chdir("doc")
        os.system("doxygen Doxyfile")
        os.system("rsync -avzP -e 'ssh -l turulomio' html/ frs.sourceforge.net:/home/users/t/tu/turulomio/userweb/htdocs/doxygen/ssh_telegram_advice/ --delete-after")
        os.chdir("..")

## Class to define uninstall command
class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system()=="Linux":
            os.system("rm -Rf {}/ssh_telegram_advice*".format(site.getsitepackages()[0]))
            os.system("rm /usr/bin/ssh_telegram_advice*")
        else:
            os.system("pip uninstall ssh_telegram_advice")

########################################################################

## Version of ssh_telegram_advice captured from commons to avoid problems with package dependencies
__version__= None
with open('ssh_telegram_advice/__init__.py', encoding='utf-8') as f:
    for line in f.readlines():
        if line.find("__version__ =")!=-1:
            __version__=line.split("'")[1]


setup(name='ssh_telegram_advice',
     version=__version__,
     description='Python app to log in Telegram ssh logins',
     long_description='Project web page is in https://github.com/turulomio/ssh_telegram_advice',
     long_description_content_type='text/markdown',
     classifiers=['Development Status :: 4 - Beta',
                  'Intended Audience :: Developers',
                  'Topic :: Software Development :: Build Tools',
                  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                  'Programming Language :: Python :: 3',
                 ], 
     keywords='ssh telegram advice logs',
     url='https://github.com/turulomio/ssh_telegram_advice',
     author='Turulomio',
     author_email='turulomio@yahoo.es',
     license='GPL-3',
     packages=['ssh_telegram_advice'],
     install_requires=[],
     entry_points = {'console_scripts': [
                            'ssh_telegram_advice=ssh_telegram_advice.core:main',
                        ],
                    },
     cmdclass={'doxygen': Doxygen,
               'uninstall':Uninstall, 
               'translate': Translate,
               'procedure': Procedure,
               'reusing': Reusing,
              },
     zip_safe=False,
     include_package_data=True
)
