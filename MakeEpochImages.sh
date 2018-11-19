#! /usr/bin/env bash


python MakeReferenceImages.py

python MakeEpochCatalogues.py

epochs=($( ls Epoch??_noise.fits ))
for e in "${epochs[@]}"
do
  echo ${e}
  AeRes -f ${e} -r ${e%%_noise.fits}.fits --add -c ${e%%_noise.fits}_comp_simp.fits
done