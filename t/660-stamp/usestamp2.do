exec >"$3"
redo-ifchange stampy
echo 2 $$ >>usestamp2.log
cat stampy
