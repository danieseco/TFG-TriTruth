from distutils.core import setup 
import py2exe 
 
setup(name="TriTruthAPP", 
 version="1.0", 
 description="Aplicacion para la verificación de la distancia de drafting en triatlon", 
 author="Daniel Seco", 
 license="PROPIA", 
 scripts=["main.py, 
 console=["main.py, 
 options={"py2exe": {"bundle_files": 1}}, 
 zipfile=None,
)