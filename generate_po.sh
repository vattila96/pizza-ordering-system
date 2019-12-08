#!/bin/sh

#put the script to the ..\pizza-ordering-system\src\app directory

output="src\locale\hu\LC_MESSAGES\test.po"
#clear output
> $output

#get all html files in dir and subdir
FILES=$(find . -type f -name '*.html')

#loop through files
for f in $FILES
do
	#search keyword in line
	i=0
	while read -r line
	do
		#search keyword in file
		(( i=$i + 1 ))
		if [[ $line == *"% trans \""* ]]
		then

			text=${line%\" %\}*}  		# retain the part before the [ " %} ] part
			text=${text##*\{% trans \"} # retain the part after the [ {% trans " ] part

			path=${f##*\.\/src\/}		# retain the part after the [ ./src/ ] part

			#add string to the .po file
			echo "#: "$path":"$i >>$output
			echo "msgid \""$text"\"" >>$output
			echo "msgstr \"\"" >>$output
			echo "" >>$output
		fi
	done <$f
done