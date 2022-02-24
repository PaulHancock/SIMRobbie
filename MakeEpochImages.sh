#! /usr/bin/env bash

dir=`python -c 'from settings import data_dir; print(data_dir)'`
mkdir -p ${dir}

ramin=`python -c 'from settings import rarange; print(rarange[0])'`
ramax=`python -c 'from settings import rarange; print(rarange[1])'`
decmax=`python -c 'from settings import decrange; print(decrange[0])'`
decmin=`python -c 'from settings import decrange; print(decrange[1])'`

echo "Making region file"
MIMAS +p ${ramin} ${decmin} ${ramax} ${decmin} ${ramax} ${decmax} ${ramin} ${decmax} -o ${dir}/square.mim
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
