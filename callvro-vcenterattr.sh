#----------------> Update vCenter attributes for various notes like Owner, DateCreated
#callvro-vcenterattr.sh vROhost.domain.com vmname owner thedate
SCNAME=$(basename $0);
if [ $# -eq 0 ]; then
	echo "ERROR: Need to provide a vROhost!"
	echo "Use it like: $SCNAME vROhost.domain.com vmname owner date"
  exit 1
fi

if [ -z "$1" ]&&[ -z "$2"]&&[ -z "$3"]&&[ -z "$4"]; then 
    echo "ERROR: Need to provide a vROhost!"
    echo "Use it like: $SCNAME vROhost.domain.com vmname owner date"
    exit 1
fi
#get workflow id for Update vCenter attr
echo "Hong Kong Update vCenter attributes"
vROhost="$(echo $1)"
user='admin'
pass='xxxxxxxx'
vmname="$(echo $2)"
owner="$(echo $3)"
thedate="$(echo $4)"
workid=$(curl -ks -u $user:$pass -X GET https://$vROhost:8281/vco/api/workflows?conditions=name=HK-Update-vCenter-attr | awk 'BEGIN { FS = "," } ; { print $1 }' | awk 'BEGIN { FS = "//" } ; { print $2 }' | awk 'BEGIN { FS = "/" } ; { print $5 }')
#get json file for POST
jsonchange="{\"parameters\":[{\"value\":{\"string\":{\"value\":\"$owner\"}},\"type\":\"string\",\"name\":\"new_owner\",\"scope\":\"local\"},{\"value\":{\"string\":{\"value\":\"$vmname\"}},\"type\":\"string\",\"name\":\"vmname\",\"scope\":\"local\"},{\"value\":{\"string\":{\"value\":\"$thedate\"}},\"type\":\"string\",\"name\":\"DateCreated\",\"scope\":\"local\"}]}"
#run the actual POST
curl -ks -u $user:$pass -H "Content-Type: application/json; Accept: application/json" -X POST -d "$jsonchange" https://$vROhost:8281/vco/api/workflows/$workid/executions

# # JSON format example:
# {
# 	"parameters":
# 	[
# 	    {
# 	        "value": {"string": {"value": owner}},
# 	        "type": "string",
# 	        "name": "owner",
# 	        "scope": "local"
# 	    },
# 	    {
# 	        "value": {"string": {"value": vmname}},
# 	        "type": "string",
# 	        "name": "vmname",
# 	        "scope": "local"
# 	    },
# 	    {
# 	        "value": {"string": {"value": thedate}},
# 	        "type": "string",
# 	        "name": "DateCreated",
# 	        "scope": "local"
# 	    }
# 	]
# }