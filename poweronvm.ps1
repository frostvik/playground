Show powered on VMs + their host
Get-vm | where { $_.PowerState -eq "PoweredOn"} | Sort-Object | Format-Table -AutoSize

#poweronvm.ps1 -VSserver name -VSusername username -VSpassword password -vmstring "*cloud*"

[CmdletBinding()]
Param(
[Parameter()]
[string]$VSserver = $(if ([string]::IsNullOrEmpty($env:VSserver)) {throw "The parameter $VSserver is required .... STOP."}),
[Parameter()]
[string]$VSusername = $(if ([string]::IsNullOrEmpty($env:VSusername)) {throw "The parameter $VSusername is required .... STOP."}),
[Parameter()]
[string]$VSpassword = $(if ([string]::IsNullOrEmpty($env:VSpassword)) {throw "The parameter $VSpassword is required .... STOP."}),
[Parameter()]
[string]$vmstring = $(if ([string]::IsNullOrEmpty($env:vmstring)) {throw "The parameter $vmstring is required .... STOP."})
)
Connect-VIServer $VSserver -User $VSusername -Password $VSpassword | out-null

if ($LastExitCode){
    write-output "The Connection to $VSserver VIServer has been completed successfully"
    }
else{
    throw "Could not connect to serve $VSserver"
    }
foreach ($vm in $(Get-VM | Sort-Object Name | where{$_.PowerState -eq "PoweredOff"} | where{$_.Name -like "$vmstring"} | Format-Table -AutoSize)){
    echo $vm | Format-Table -AutoSize
    #Start-Vm -VM $vm.name -Confirm:$false
    }
Disconnect-VIServer * -Confirm:$FALSE