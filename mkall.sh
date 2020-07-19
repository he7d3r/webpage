#!/bin/bash

##################################################
#
# Compila e instala todo o site!
#
# Autor: Pedro H A Konzen - UFRGS - 01/2018
#
##################################################

#portal REAMAT
python3.5 mkwp.py

./mkAlgebraLinear.sh &
./mkCalculo.sh &
./mkCalculoNumerico.sh &
./mkComputacaoCientifica.sh &
./mkPreCalculo.sh &
./mkTransformadasIntegrais.sh &

echo "Congratulations! You may now update the server. :)"
