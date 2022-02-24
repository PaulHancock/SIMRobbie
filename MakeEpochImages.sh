#! /usr/bin/env bash

dir=`python -c 'from settings import data_dir; print(data_dir)'`

echo "Making region file"
MIMAS +p 173 -7 187 -7 187 7 173 7 -o ${dir}/square.mim
MIMAS --mim2reg ${dir}/square.mim ${dir}/square.reg

echo "Making reference images"
python MakeReferenceImages.py || exit

echo "Making Catalogues"
python MakeEpochCatalogues.py || exit

echo "Populating images"
epochs=($( ls ${dir}/Epoch??_noise.fits ))
for e in "${epochs[@]}"
do
  echo ${e}
  AeRes -f ${e} -r ${e%%_noise.fits}.fits --add -c ${e%%_noise.fits}_comp_simp.fits || exit
done
