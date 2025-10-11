# encoding  utf-8


PATH_TEMPLATE='/Users/martinkern/Documents/GitHub/Script_Therion'

if [ -z "$1" ]
then
      echo "\$var is empty"
      echo "Give name to your survey"
      read S
else
      echo "\$var is NOT empty"
      S=$1
fi

echo "Creating survey folder for : $S"
mkdir $S
cd $S
mkdir exports
mkdir datas

sed "s/<CAVENAME>/$S/g" ${PATH_TEMPLATE}/Therion_files_pattern/CAVENAME_map.th > ${S}_map.th
sed "s/<CAVENAME>/$S/g" ${PATH_TEMPLATE}/Therion_files_pattern/CAVENAME_tot.th > ${S}_tot.th
sed "s/<CAVENAME>/$S/g" ${PATH_TEMPLATE}/Therion_files_pattern/CAVENAME_CONFIG.thconfig > CAVENAME_CONFIG.thconfig
sed "s/<CAVENAME>/$S/g" ${PATH_TEMPLATE}/Therion_files_pattern/config-xvi.thcfg > config-xvi.thcfg

cd datas
sed "s/<CAVENAME>/$S/g" ${PATH_TEMPLATE}/Therion_files_pattern/CAVENAME_P.th2 > ${S}_P.th2
sed "s/<CAVENAME>/$S/g" ${PATH_TEMPLATE}/Therion_files_pattern/CAVENAME_C.th2 > ${S}_C.th2


cd ..
