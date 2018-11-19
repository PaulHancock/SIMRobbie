#! /usr/bin/env bash

# MIMAS +p 173 -7 187 -7 187 7 173 7 -o square.mim
# MIMAS --mim2reg square.mim square.reg

python MakeReferenceImages.py

python MakeEpochCatalogues.py

epochs=($( ls Epoch??_noise.fits ))
for e in "${epochs[@]}"
do
  echo ${e}
  AeRes -f ${e} -r ${e%%_noise.fits}.fits --add -c ${e%%_noise.fits}_comp_simp.fits
done